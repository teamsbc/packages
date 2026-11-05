import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET


spec = importlib.util.spec_from_file_location(
    "package_repository", Path(__file__).parents[1] / "package_repository.py"
)
repository = importlib.util.module_from_spec(spec)
spec.loader.exec_module(repository)

try:
    import createrepo_c as cr
except ImportError:
    cr = None


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "sources"
        self.root.mkdir()
        self.metadata = Path(self.temp.name) / "repomd.xml"
        self.git("init", "-q")
        for package in ("common/alpha", "common/beta", "firmware/uboot"):
            self.write(f"{package}/package.spec")
        self.baseline = self.commit()
        self.record(self.baseline)

    def git(self, *args):
        return repository.git(self.root, *args).strip()

    def write(self, path, content="fixture\n"):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)

    def commit(self):
        self.git("add", "-A")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.org",
                 "-c", "commit.gpgsign=false",
                 "commit", "-qm", "fixture")
        return self.git("rev-parse", "HEAD")

    def record(self, revision):
        self.metadata.write_text(
            f'<repomd xmlns="{repository.REPOMD_NS}"><revision>{revision}</revision></repomd>'
        )

    def select(self, name="common", force=False):
        return repository.select_packages(self.root, name, self.metadata, force)

    def test_sources_and_multiple_unpublished_commits(self):
        self.write("common/alpha/policy.te")
        self.commit()
        # An intervening failed or skipped run has not advanced repomd.xml.
        self.write("common/beta/config")
        self.write("firmware/uboot/patch")
        self.commit()
        self.assertEqual(self.select(), ["common/alpha", "common/beta"])
        self.assertEqual(self.select("firmware"), ["firmware/uboot"])

    def test_unchanged_repository_and_documentation_are_skipped(self):
        self.write("README.md")
        self.write("firmware/uboot/patch")
        self.commit()
        self.assertEqual(self.select(), [])

    def test_shared_build_inputs_rebuild_every_package(self):
        for path in (".github/workflows/build.yml", ".github/scripts/helper.py", "common/shared"):
            with self.subTest(path=path):
                self.write(path)
                self.commit()
                self.assertEqual(self.select(), ["common/alpha", "common/beta"])
                self.record(self.git("rev-parse", "HEAD"))

    def test_rename_rebuilds_both_source_directories(self):
        self.write("common/alpha/source")
        self.record(self.commit())
        (self.root / "common/alpha/source").rename(self.root / "common/beta/source")
        self.commit()
        self.assertEqual(self.select(), ["common/alpha", "common/beta"])

    def test_deleted_packages_are_ignored(self):
        (self.root / "common/alpha/package.spec").unlink()
        self.commit()
        self.assertEqual(self.select(), [])

    def test_missing_legacy_and_unknown_baselines_rebuild_all(self):
        self.metadata.unlink()
        self.assertEqual(self.select(), ["common/alpha", "common/beta"])
        for revision in ("1234567890", "0" * 40):
            with self.subTest(revision=revision):
                self.record(revision)
                self.assertEqual(self.select(), ["common/alpha", "common/beta"])

    def test_manual_rebuild_includes_unchanged_packages(self):
        self.assertEqual(self.select(), [])
        self.assertEqual(self.select(force=True), ["common/alpha", "common/beta"])

    def test_old_rerun_cannot_replace_a_newer_publication(self):
        self.write("common/alpha/source")
        newer = self.commit()
        self.git("checkout", "-q", "--detach", self.baseline)
        self.record(newer)
        self.assertEqual(self.select(), [])
        self.assertEqual(self.select(force=True), [])

    def test_rewritten_history_rebuilds_all(self):
        self.write("common/alpha/source")
        self.record(self.commit())
        self.git("checkout", "-q", "--detach", self.baseline)
        self.write("common/beta/source")
        self.commit()
        self.assertEqual(self.select(), ["common/alpha", "common/beta"])


class FetchTests(unittest.TestCase):
    @patch.object(repository.subprocess, "run")
    @patch.object(repository.subprocess, "check_output")
    def test_fetches_only_referenced_metadata(self, check_output, run):
        check_output.return_value = json.dumps(["main/latest/repodata/repomd.xml"]).encode()
        manifest = (
            f'<repomd xmlns="{repository.REPOMD_NS}">'
            '<data type="primary"><location href="repodata/primary.xml.gz"/></data>'
            '<data type="filelists"><location href="repodata/filelists.xml.gz"/></data>'
            '</repomd>'
        )

        def download(args, check):
            Path(args[4]).write_text(manifest if args[3].endswith("repomd.xml") else "metadata")

        run.side_effect = download
        with tempfile.TemporaryDirectory() as temp:
            repository.fetch_metadata("s3://bucket/main/latest", Path(temp))
        self.assertEqual([call.args[0][3] for call in run.call_args_list], [
            "s3://bucket/main/latest/repodata/repomd.xml",
            "s3://bucket/main/latest/repodata/primary.xml.gz",
            "s3://bucket/main/latest/repodata/filelists.xml.gz",
        ])

    @patch.object(repository.subprocess, "run")
    @patch.object(repository.subprocess, "check_output", return_value=b"null")
    def test_missing_repository_needs_no_download(self, check_output, run):
        with tempfile.TemporaryDirectory() as temp:
            repository.fetch_metadata("s3://bucket/main/latest", Path(temp))
        run.assert_not_called()

    @patch.object(repository.subprocess, "check_output",
                  side_effect=subprocess.CalledProcessError(1, "aws"))
    def test_storage_errors_fail_instead_of_using_an_empty_repository(self, check_output):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(subprocess.CalledProcessError):
                repository.fetch_metadata("s3://bucket/main/latest", Path(temp))


class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        (self.directory / "repodata").mkdir()
        (self.directory / "repodata/repomd.xml").write_text(
            f'<repomd xmlns="{repository.REPOMD_NS}">'
            '<data type="primary"><location href="repodata/primary.xml"/></data>'
            '<data type="filelists"><location href="repodata/filelists.xml"/></data>'
            '</repomd>'
        )
        (self.directory / "repodata/primary.xml").write_text(
            f'<metadata xmlns="{repository.PRIMARY_NS}" packages="1">'
            '<package><location href="packages/current.rpm"/></package></metadata>'
        )
        self.prefix = "main/latest/46/x86_64/common/"
        self.objects = [self.prefix + name for name in (
            "repodata/repomd.xml", "repodata/primary.xml", "repodata/filelists.xml",
            "packages/current.rpm", "old.rpm", "repodata/old.xml.gz", "index.html",
        )]

    @patch.object(repository, "fetch_metadata")
    @patch.object(repository.subprocess, "check_output")
    def test_removes_only_unreferenced_rpms_and_metadata(self, check_output, fetch):
        check_output.side_effect = [
            json.dumps({"Contents": [{"Key": key} for key in self.objects]}).encode(),
            b'{}',
        ]
        repository.cleanup_repository("s3://bucket/" + self.prefix, self.directory)
        args = check_output.call_args_list[1].args[0]
        self.assertEqual(json.loads(args[args.index("--delete") + 1])["Objects"], [
            {"Key": self.prefix + "old.rpm"},
            {"Key": self.prefix + "repodata/old.xml.gz"},
        ])

    @patch.object(repository, "fetch_metadata")
    @patch.object(repository.subprocess, "check_output")
    def test_empty_quiet_delete_response_succeeds(self, check_output, fetch):
        check_output.side_effect = [
            json.dumps({"Contents": [{"Key": key} for key in self.objects]}).encode(),
            b"",
        ]
        repository.cleanup_repository("s3://bucket/" + self.prefix, self.directory)
        self.assertEqual(check_output.call_count, 2)

    @unittest.skipUnless(shutil.which("zstd"), "zstd is required")
    @patch.object(repository, "fetch_metadata")
    def test_reads_zstd_primary_metadata(self, fetch):
        primary = self.directory / "repodata/primary.xml"
        subprocess.run(["zstd", "-q", str(primary), "-o", str(primary) + ".zst"], check=True)
        manifest = self.directory / "repodata/repomd.xml"
        manifest.write_text(manifest.read_text().replace("primary.xml", "primary.xml.zst"))
        self.objects = [key.replace("primary.xml", "primary.xml.zst") for key in self.objects]
        original = subprocess.check_output

        def command(args):
            if args[0] == "zstd":
                return original(args)
            if args[1] == "s3api" and args[2] == "list-objects-v2":
                return json.dumps({"Contents": [{"Key": key} for key in self.objects]}).encode()
            return b"{}"

        with patch.object(repository.subprocess, "check_output", side_effect=command):
            repository.cleanup_repository("s3://bucket/" + self.prefix, self.directory)

    @patch.object(repository, "fetch_metadata")
    @patch.object(repository.subprocess, "check_output")
    def test_missing_referenced_object_prevents_deletion(self, check_output, fetch):
        check_output.return_value = json.dumps({"Contents": [
            {"Key": key} for key in self.objects if not key.endswith("current.rpm")
        ]}).encode()
        with self.assertRaises(ValueError):
            repository.cleanup_repository("s3://bucket/" + self.prefix, self.directory)
        self.assertEqual(check_output.call_count, 1)

    @patch.object(repository, "fetch_metadata")
    @patch.object(repository.subprocess, "check_output")
    def test_invalid_primary_prevents_deletion(self, check_output, fetch):
        (self.directory / "repodata/primary.xml").write_text("<invalid/>")
        with self.assertRaises(ValueError):
            repository.cleanup_repository("s3://bucket/" + self.prefix, self.directory)
        check_output.assert_not_called()

    @patch.object(repository, "fetch_metadata")
    @patch.object(repository.subprocess, "check_output")
    def test_delete_errors_fail_cleanup(self, check_output, fetch):
        check_output.side_effect = [
            json.dumps({"Contents": [{"Key": key} for key in self.objects]}).encode(),
            b'{"Errors": [{"Key": "old.rpm", "Code": "AccessDenied"}]}',
        ]
        with self.assertRaises(RuntimeError):
            repository.cleanup_repository("s3://bucket/" + self.prefix, self.directory)


@unittest.skipUnless(cr is not None and shutil.which("createrepo_c") and shutil.which("mergerepo_c"),
                     "createrepo_c, mergerepo_c and Python bindings are required")
class MergeTests(unittest.TestCase):
    def fixture(self, directory, packages):
        writer = cr.RepositoryWriter(str(directory), num_packages=len(packages))
        for name, version in packages:
            package = cr.Package()
            package.name, package.version = name, version
            package.arch, package.epoch, package.release = "noarch", "0", "1"
            package.pkgId, package.checksum_type = (name + version).encode().hex().ljust(64, "0"), "sha256"
            package.location_href = f"{name}-{version}-1.noarch.rpm"
            package.rpm_sourcerpm = f"{name}-{version}-1.src.rpm"
            writer.add_pkg(package)
        writer.finish()

    def load(self, directory):
        metadata = cr.Metadata(cr.HT_KEY_NAME)
        metadata.locate_and_load_xml(str(directory))
        return {name: metadata.get(name) for name in metadata.keys()}

    def test_merge_replaces_changed_packages_without_old_rpms(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            old, new, merged = root / "old", root / "new", root / "merged"
            self.fixture(old, [("unchanged", "1"), ("changed", "1"), ("removed", "1")])
            self.fixture(new, [("changed", "2")])
            subprocess.run(["mergerepo_c", "--repo", str(new), "--repo", str(old),
                            "--method", "repo", "--omit-baseurl", "--no-database",
                            "--outputdir", str(merged)], check=True, capture_output=True)
            packages = self.load(merged)
            self.assertEqual({name: pkg.version for name, pkg in packages.items()},
                             {"unchanged": "1", "changed": "2", "removed": "1"})
            self.assertTrue(all(not pkg.location_base for pkg in packages.values()))
            self.assertEqual(packages["changed"].location_href, "changed-2-1.noarch.rpm")
            self.assertFalse(list(root.rglob("*.rpm")))

    def test_publish_records_commit_for_both_bootstrap_and_merge(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            old, new = root / "old", root / "new"
            new.mkdir()
            revision = "a" * 40
            for existing in (False, True):
                with self.subTest(existing=existing):
                    if existing:
                        self.fixture(old, [("unchanged", "1")])
                    output = root / str(existing)
                    repository.merge_metadata(new, old, output, revision)
                    manifest = ET.parse(output / "repodata/repomd.xml")
                    self.assertEqual(manifest.findtext(f"{{{repository.REPOMD_NS}}}revision"), revision)
                    self.assertEqual(set(self.load(output)), {"unchanged"} if existing else set())


if __name__ == "__main__":
    unittest.main()
