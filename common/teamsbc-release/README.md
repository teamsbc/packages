# Lhotse kernel images

Lhotse generates a Unified Kernel Image (UKI) for each installed kernel. DNF
continues to manage kernel RPMs. Their `kernel-install` calls use dracut to
generate the initramfs and ukify to combine it with the kernel and systemd stub.
systemd-boot discovers the resulting images in `/boot/EFI/Linux/`.

Entry names contain `IMAGE_ID` and the kernel version so multiple installed
kernels remain independently bootable. `/etc/kernel/tries` enables boot counting.
The Lhotse identity package requires the generation tools and ships a cleanup
hook because Fedora's kernel-core RPM requests Type 1 cleanup even when its
kernel has been installed as a locally generated UKI. The hook delegates to
systemd's UKI plugin to remove the image, boot-counter variants, and extras.

To change kernel arguments, write `/etc/kernel/cmdline` and regenerate the UKIs:

```console
run0 kernel-install add-all
```

The arguments are embedded when each UKI is generated. Keep the required local
boot arguments when editing the command line.

Run the cleanup checks on a system with systemd's `90-uki-copy.install` plugin:

```console
python3 -m unittest discover -s common/teamsbc-release/tests -v
```
