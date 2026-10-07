#!/usr/bin/env python3
"""Select package sources and update rpm-md repositories without fetching RPMs."""

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET


REPOMD_NS = "http://linux.duke.edu/metadata/repo"


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args]).decode()


def select_packages(root, repository, metadata, force=False):
    packages = sorted({str(spec.parent.relative_to(root))
                       for spec in (root / repository).glob("*/*.spec")})
    baseline = None
    if metadata.is_file():
        baseline = ET.parse(metadata).findtext(f"{{{REPOMD_NS}}}revision")
    if not baseline or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", baseline):
        return packages

    if subprocess.run(
        ["git", "-C", str(root), "cat-file", "-e", f"{baseline}^{{commit}}"],
        check=False, stderr=subprocess.DEVNULL,
    ).returncode != 0:
        return packages

    head = git(root, "rev-parse", "HEAD").strip()
    if baseline != head and subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", head, baseline],
        check=False,
    ).returncode == 0:
        print("A newer commit is already published; skipping this older run.", file=sys.stderr)
        return []
    if force:
        return packages
    if subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", baseline, head],
        check=False,
    ).returncode != 0:
        return packages

    changed = git(root, "diff", "--name-only", "--no-renames", "-z", baseline, head).split("\0")
    if any(path == ".github/workflows/build.yml" or path.startswith(".github/scripts/")
           or path.startswith(f"{repository}/") and len(path.split("/")) == 2
           for path in changed):
        return packages
    return [package for package in packages
            if any(path.startswith(f"{package}/") for path in changed)]


def fetch_metadata(uri, directory):
    """Fetch repomd.xml and only the metadata files it references from R2."""
    location = urlsplit(uri)
    if location.scheme != "s3" or not location.netloc:
        raise ValueError("Expected an s3:// repository URL")
    key = f"{location.path.strip('/')}/repodata/repomd.xml"
    keys = json.loads(subprocess.check_output([
        "aws", "s3api", "list-objects-v2", "--bucket", location.netloc,
        "--prefix", key, "--query", "Contents[].Key", "--output", "json",
    ])) or []
    if key not in keys:
        return

    def download(href):
        path = PurePosixPath(href)
        if path.is_absolute() or ".." in path.parts or urlsplit(href).scheme:
            raise ValueError(f"Metadata path must be relative: {href}")
        target = directory / path
        target.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["aws", "s3", "cp", f"{uri.rstrip('/')}/{href}",
                        str(target), "--no-progress"], check=True)

    download("repodata/repomd.xml")
    for item in ET.parse(directory / "repodata/repomd.xml").findall(
        f"{{{REPOMD_NS}}}data/{{{REPOMD_NS}}}location"
    ):
        download(item.attrib["href"])


def merge_metadata(new, old, output, revision):
    subprocess.run(["createrepo_c", "--revision", revision, str(new)], check=True)
    if (old / "repodata/repomd.xml").is_file():
        subprocess.run([
            "mergerepo_c", "--repo", str(new), "--repo", str(old),
            "--method", "repo", "--omit-baseurl", "--no-database",
            "--outputdir", str(output),
        ], check=True)
    else:
        shutil.copytree(new / "repodata", output / "repodata")

    # mergerepo_c generates a timestamp revision. Record the published source
    # commit in the same object that makes the merged metadata visible to DNF.
    manifest = output / "repodata/repomd.xml"
    tree = ET.parse(manifest)
    revision_element = tree.find(f"{{{REPOMD_NS}}}revision")
    if revision_element is None:
        revision_element = ET.SubElement(tree.getroot(), f"{{{REPOMD_NS}}}revision")
    revision_element.text = revision
    ET.register_namespace("", REPOMD_NS)
    ET.register_namespace("rpm", "http://linux.duke.edu/metadata/rpm")
    tree.write(manifest, encoding="utf-8", xml_declaration=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    fetch = commands.add_parser("fetch")
    fetch.add_argument("uri")
    fetch.add_argument("directory", type=Path)
    select = commands.add_parser("select")
    select.add_argument("repository", choices=["common", "firmware"])
    select.add_argument("metadata", type=Path)
    select.add_argument("--force", action="store_true")
    merge = commands.add_parser("merge")
    merge.add_argument("new", type=Path)
    merge.add_argument("old", type=Path)
    merge.add_argument("output", type=Path)
    merge.add_argument("revision")
    args = parser.parse_args()
    if args.command == "fetch":
        fetch_metadata(args.uri, args.directory)
    elif args.command == "select":
        for package in select_packages(Path.cwd(), args.repository, args.metadata, args.force):
            print(package)
    else:
        merge_metadata(args.new, args.old, args.output, args.revision)


if __name__ == "__main__":
    main()
