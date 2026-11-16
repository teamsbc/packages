#!/usr/bin/python3
"""Update all kernel SRPM pins from the Fedora 46 Rawhide source repository."""

import hashlib
from pathlib import Path
import re
import subprocess
import tempfile

import rpm

ROOT = Path(__file__).resolve().parents[2]
PINS = [ROOT / name / 'kernel/source.env' for name in ('virt', 'rpi4', 'rpi5')]
KEY = '/usr/share/pki/rpm-gpg/RPM-GPG-KEY-fedora-46-primary'
KOJI = 'https://kojipkgs.fedoraproject.org/packages/kernel'


def command(*args):
    return subprocess.check_output(args, text=True).strip()


def read_pin(path):
    values = {}
    for line in path.read_text().splitlines():
        if line and not line.startswith('#'):
            key, value = line.split('=', 1)
            if key not in ('SRPM_URL', 'SRPM_SHA256') or key in values:
                raise ValueError(f'Invalid pin in {path}: {line}')
            values[key] = value
    if set(values) != {'SRPM_URL', 'SRPM_SHA256'}:
        raise ValueError(f'Incomplete pin: {path}')
    return values


def main():
    pins = [read_pin(path) for path in PINS]
    if any(pin != pins[0] for pin in pins[1:]):
        raise ValueError('Kernel pins differ; reconcile them before updating')
    old = re.fullmatch(rf'{KOJI}/([^/]+)/([^/]+)/data/signed/91211fce/src/kernel-\1-\2\.src\.rpm', pins[0]['SRPM_URL'])
    if not old or not re.fullmatch(r'[0-9a-f]{64}', pins[0]['SRPM_SHA256']):
        raise ValueError('Unexpected current Fedora kernel pin')

    result = command('dnf5', '--quiet', '--refresh', '--disablerepo=*',
                     '--enablerepo=rawhide-source', 'repoquery', '--available',
                     '--arch=src', '--latest-limit=1',
                     '--queryformat=%{name} %{epoch} %{version} %{release}', 'kernel')
    lines = result.splitlines()
    if len(lines) != 1:
        raise ValueError(f'Expected one source package, got: {result!r}')
    name, epoch, version, release = lines[0].split()
    if (name != 'kernel' or epoch not in ('0', '(none)')
            or not re.fullmatch(r'[A-Za-z0-9._+~]+', version)
            or not re.fullmatch(r'[A-Za-z0-9._+~]+\.fc46', release)):
        raise ValueError(f'Unexpected source package: {result}')
    comparison = rpm.labelCompare(('0', version, release), ('0', old[1], old[2]))
    if comparison < 0:
        raise ValueError('Fedora source repository is older than the current pin')
    if comparison == 0:
        print('Kernel source is already current')
        return
    url = f'{KOJI}/{version}/{release}/data/signed/91211fce/src/kernel-{version}-{release}.src.rpm'
    with tempfile.TemporaryDirectory() as temp:
        srpm = Path(temp) / 'kernel.src.rpm'
        db = Path(temp) / 'rpmdb'
        db.mkdir()
        subprocess.run(['curl', '--fail', '--location', '--retry', '3', '--output', str(srpm), url], check=True)
        subprocess.run(['rpm', '--dbpath', str(db), '--initdb'], check=True)
        subprocess.run(['rpm', '--dbpath', str(db), '--import', KEY], check=True)
        verification = command('rpmkeys', '--dbpath', str(db), '--checksig', '--verbose', str(srpm))
        if not re.search(r'(?im)^\s*.*signature.*: OK\s*$', verification):
            raise ValueError(f'No valid Fedora signature: {verification}')
        identity = command('rpm', '--dbpath', str(db), '-qp', '--qf', '%{NAME} %{EPOCHNUM} %{VERSION} %{RELEASE} %{SOURCEPACKAGE}', str(srpm))
        if identity != f'kernel 0 {version} {release} 1':
            raise ValueError(f'Unexpected SRPM identity: {identity}')
        with srpm.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    content = f'# Fedora 46 source RPM, signature verified against the Fedora 46 key.\nSRPM_URL={url}\nSRPM_SHA256={digest}\n'
    for path in PINS:
        path.write_text(content)
    print(f'Updated kernel source to {version}-{release}')


if __name__ == '__main__':
    main()
