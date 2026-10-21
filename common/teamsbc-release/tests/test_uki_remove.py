"""Exercise Lhotse's cleanup hook with the installed systemd UKI plugin."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


HOOK = Path(__file__).resolve().parents[1] / "91-teamsbc-uki-remove.install"
UKI_COPY = Path("/usr/lib/kernel/install.d/90-uki-copy.install")


@unittest.skipUnless(UKI_COPY.is_file(), "systemd's UKI copy plugin is required")
class UKIRemovalTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="teamsbc-uki-test-")
        self.addCleanup(directory.cleanup)
        self.boot = Path(directory.name)
        self.ukis = self.boot / "EFI/Linux"
        self.ukis.mkdir(parents=True)
        self.env = {
            **os.environ,
            "KERNEL_INSTALL_BOOT_ROOT": str(self.boot),
            "KERNEL_INSTALL_LAYOUT": "uki",
            "KERNEL_INSTALL_UKI_GENERATOR": "ukify",
            "KERNEL_INSTALL_BOOT_ENTRY_TYPE": "type1",
            "KERNEL_INSTALL_ENTRY_TOKEN": "teamsbc-lhotse-virt",
            "KERNEL_INSTALL_ENTRY_NAME": "teamsbc-lhotse-virt_1.0",
            "KERNEL_INSTALL_VERBOSE": "0",
        }
        self.owned = [
            "teamsbc-lhotse-virt_1.0.efi",
            "teamsbc-lhotse-virt_1.0+3.efi",
            "teamsbc-lhotse-virt_1.0+2-1.efi",
            "teamsbc-lhotse-virt_1.0+0-3.efi",
        ]
        self.retained = [
            "teamsbc-lhotse-virt_1.0.1.efi",
            "teamsbc-lhotse-virt_2.0+3.efi",
            "another-os_1.0.efi",
        ]
        for name in self.owned + self.retained:
            (self.ukis / name).touch()
        self.extras = self.ukis / "teamsbc-lhotse-virt_1.0.efi.extra.d"
        self.extras.mkdir()
        (self.extras / "test.addon.efi").touch()

    def run_hook(self, command="remove", **overrides):
        subprocess.run(
            ["sh", str(HOOK), command, "1.0", str(self.boot / "entry"), ""],
            env=self.env | overrides,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_fedora_kernel_removal_cleans_uki_counters_and_extras(self):
        self.run_hook()
        self.assertEqual(sorted(p.name for p in self.ukis.iterdir()), sorted(self.retained))
        self.run_hook()  # Cleanup is safe when the UKI is already absent.

    def test_other_operations_and_configurations_leave_files_alone(self):
        cases = [
            ("add", {}),
            ("remove", {"KERNEL_INSTALL_LAYOUT": "bls"}),
            ("remove", {"KERNEL_INSTALL_UKI_GENERATOR": "dracut"}),
            ("remove", {"KERNEL_INSTALL_BOOT_ENTRY_TYPE": "type2"}),
            ("remove", {"KERNEL_INSTALL_BOOT_ENTRY_TYPE": ""}),
        ]
        before = sorted(self.ukis.rglob("*"))
        for command, overrides in cases:
            with self.subTest(command=command, overrides=overrides):
                self.run_hook(command, **overrides)
                self.assertEqual(sorted(self.ukis.rglob("*")), before)


if __name__ == "__main__":
    unittest.main()
