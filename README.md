> [!IMPORTANT]
> Issues for this repository are tracked at the [distribution bug tracker](https://github.com/teamsbc/distribution/issues).

# Packages

This repository contains the RPM packages for the [TeamSBC Remix](https://teamsbc.org/). The packages are built in GitHub Actions and uploaded to the repositories on merge to `main`.

## Repositories

Packages end up in a few different repositories.

### Common

The `common` repository contains packages that are used by all TeamSBC variants.

- `teamsbc-release`
- `teamsbc-repos`
- `teamsbc-config`
- `teamsbc-selinux`

## Firmware

The `firmware` repository contains firmware for various boards currently it contains the TeamSBC builds of u-boot which has subpackages per supported board.

- `teamsbc-uboot`.

## Package Signing

All RPMs are signed with the TeamSBC GPG key. The public key is shipped in the `teamsbc-repos` package and installed to `/etc/pki/rpm-gpg/RPM-GPG-KEY-teamsbc`.

**Fingerprint:** `C171 94E3 2B91 4884 DEBB F250 C55F 3AC4 FD3F 8B75`

To manually import the key:

```
sudo rpm --import https://packages.teamsbc.net/RPM-GPG-KEY-teamsbc
```
