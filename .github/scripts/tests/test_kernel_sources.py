import hashlib
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location('kernel_sources', ROOT / '.github/scripts/update-kernel-sources.py')
updater = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(updater)


class KernelSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pins = []
        for variant in ('virt', 'rpi4', 'rpi5'):
            directory = self.root / variant / 'kernel'
            directory.mkdir(parents=True)
            shutil.copy(ROOT / variant / 'kernel/source.env', directory)
            self.pins.append(directory / 'source.env')

    def test_update_checks_signature_and_updates_all_pins(self):
        content = b'example signed source rpm'
        def run(args, check):
            if args[0] == 'curl':
                Path(args[args.index('--output') + 1]).write_bytes(content)
        def command(*args):
            if args[0] == 'dnf5':
                return 'kernel 0 7.4.1 1.fc46'
            if args[0] == 'rpmkeys':
                return 'Header signature: OK\nPayload digest: OK'
            return 'kernel 0 7.4.1 1.fc46 1'
        with patch.object(updater, 'PINS', self.pins), patch.object(updater, 'command', command), patch.object(updater.subprocess, 'run', side_effect=run):
            updater.main()
        pins = [updater.read_pin(path) for path in self.pins]
        self.assertEqual(pins[0], pins[1])
        self.assertEqual(pins[0], pins[2])
        self.assertEqual(pins[0]['SRPM_SHA256'], hashlib.sha256(content).hexdigest())
        self.assertIn('/7.4.1/1.fc46/', pins[0]['SRPM_URL'])

    def test_rejects_diverged_pins(self):
        self.pins[1].write_text(self.pins[1].read_text().replace('ae6521', 'be6521'))
        with patch.object(updater, 'PINS', self.pins), self.assertRaisesRegex(ValueError, 'pins differ'):
            updater.main()

    def test_rejects_unsigned_candidate_without_modifying_pins(self):
        original = [p.read_text() for p in self.pins]
        def run(args, check):
            if args[0] == 'curl':
                Path(args[args.index('--output') + 1]).write_bytes(b'unsigned')
        def command(*args):
            return 'kernel 0 7.4.1 1.fc46' if args[0] == 'dnf5' else 'Payload digest: OK'
        with patch.object(updater, 'PINS', self.pins), patch.object(updater, 'command', command), patch.object(updater.subprocess, 'run', side_effect=run), self.assertRaisesRegex(ValueError, 'No valid Fedora signature'):
            updater.main()
        self.assertEqual(original, [p.read_text() for p in self.pins])

    def test_each_prepare_reads_its_own_pin(self):
        bindir = self.root / 'bin'
        bindir.mkdir()
        for name, script in {'curl': 'while [ "$1" != --output ]; do shift; done; printf data > "$2"', 'rpm': 'while [ "$1" != --define ]; do shift; done; mkdir -p "${2#_topdir }/SOURCES"'}.items():
            executable = bindir / name
            executable.write_text('#!/bin/sh\n' + script + '\n')
            executable.chmod(0o755)
        for variant in ('virt', 'rpi4', 'rpi5'):
            with self.subTest(variant=variant):
                directory = self.root / variant / 'kernel'
                shutil.copy(ROOT / variant / 'kernel/prepare', directory)
                (directory / 'source.env').write_text('SRPM_URL=https://example.invalid/source.rpm\nSRPM_SHA256=' + hashlib.sha256(b'data').hexdigest() + '\n')
                build = self.root / (variant + '-build')
                build.mkdir()
                subprocess.run(['bash', str(directory / 'prepare'), str(build)], check=True, env=dict(os.environ, PATH=f'{bindir}:{os.environ["PATH"]}'), capture_output=True)
                self.assertIn(f'buildid .teamsbc.{variant}\n', (build / '.build-args').read_text())
                self.assertIn('# CONFIG_SECURITY_SELINUX is not set\n', (build / 'SOURCES/kernel-local').read_text())
                self.assertIn('CONFIG_NETWORK_SECMARK=y\n', (build / 'SOURCES/kernel-local').read_text())
                self.assertTrue((build / '.prepared').exists())


if __name__ == '__main__':
    unittest.main()
