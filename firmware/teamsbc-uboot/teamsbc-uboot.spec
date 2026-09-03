%global candidate rc3
%global uboot_version %{version}%{?candidate:-%{candidate}}
# No ELF binaries, only firmware blobs; disable empty debuginfo/debugsource packages
%global debug_package %{nil}

Name:     teamsbc-uboot
Version:  2026.10
Release:  4%{?candidate:.%{candidate}}%{?dist}
Summary:  U-Boot firmware images for TeamSBC
License:  GPL-2.0-or-later AND LicenseRef-Callaway-BSD AND LGPL-2.1-or-later AND LGPL-2.0-or-later
URL:      https://u-boot-project.org/
ExclusiveArch: aarch64

Source0:  https://git.u-boot-project.org/u-boot/u-boot/-/archive/v%{uboot_version}/u-boot-v%{uboot_version}.tar.bz2
Source1:  rpi4-tpm-measured-boot.config
Source2:  rpi4-tpm-spi-gpio.dts

Patch0:   enable-bootmenu-by-default.patch
Patch1:   disable-VBE-by-default.patch
Patch2:   uefi-enable-SetVariableRT-with-volotile-storage.patch

BuildRequires: bc
BuildRequires: bison
BuildRequires: dtc
BuildRequires: flex
BuildRequires: gcc
BuildRequires: gnutls-devel
BuildRequires: libuuid-devel
BuildRequires: make
BuildRequires: ncurses-devel
%if 0%{?fedora} > 44
BuildRequires: openssl3-devel
BuildRequires: openssl3-devel-engine
%else
BuildRequires: openssl-devel
BuildRequires: openssl-devel-engine
%endif
BuildRequires: perl-interpreter
BuildRequires: python3-devel
BuildRequires: python3-libfdt
BuildRequires: python3-pyelftools
BuildRequires: python3-setuptools
BuildRequires: SDL2-devel
BuildRequires: swig
BuildRequires: xxd

%description
U-Boot firmware images for TeamSBC supported boards.

%package rpi4
Summary:  U-Boot firmware for Raspberry Pi 4
BuildArch: noarch

%description rpi4
U-Boot firmware image for Raspberry Pi 4.

%package rpi4-letstrust
Summary:  LetsTrust TPM overlay for Raspberry Pi 4
BuildArch: noarch
Requires: %{name}-rpi4 = %{version}-%{release}

%description rpi4-letstrust
Device tree overlay for the LetsTrust TPM module (Infineon SLB9672) on
Raspberry Pi 4. Enables the TPM via SPI GPIO bitbanging for use with
U-Boot measured boot (EFI TCG2) and Linux.

%package rpi5
Summary:  U-Boot firmware for Raspberry Pi 5
BuildArch: noarch

%description rpi5
U-Boot firmware image for Raspberry Pi 5.

%prep
%autosetup -p1 -n u-boot-v%{uboot_version}

%build
# Both RPi 4 and RPi 5 use the unified rpi_arm64 defconfig
mkdir -p builds/rpi_arm64
make rpi_arm64_defconfig O=builds/rpi_arm64/
# Merge TPM2 measured boot config fragment
./scripts/kconfig/merge_config.sh -m -O builds/rpi_arm64/ builds/rpi_arm64/.config %{SOURCE1}
make olddefconfig O=builds/rpi_arm64/
%make_build HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" O=builds/rpi_arm64/

# Compile TPM SPI GPIO device tree overlay
dtc -@ -I dts -O dtb -o letstrust-tpm-spi-gpio.dtbo %{SOURCE2}

%install
for board in rpi4 rpi5; do
  install -pDm 0644 builds/rpi_arm64/u-boot.bin \
    %{buildroot}%{_datadir}/%{name}/${board}/u-boot.bin
done
install -pDm 0644 letstrust-tpm-spi-gpio.dtbo \
  %{buildroot}%{_datadir}/%{name}/rpi4/letstrust-tpm-spi-gpio.dtbo

%files rpi4
%license Licenses/gpl-2.0.txt
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/rpi4/
%{_datadir}/%{name}/rpi4/u-boot.bin

%files rpi4-letstrust
%license Licenses/gpl-2.0.txt
%{_datadir}/%{name}/rpi4/letstrust-tpm-spi-gpio.dtbo

%files rpi5
%license Licenses/gpl-2.0.txt
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/rpi5/

%changelog
* Thu Sep 03 2026 Simon de Vlieger <cmdr@supakeen.com> - 2026.10-4.rc3
- Enable TPM2 measured boot (EFI TCG2) via Kconfig fragment.
- Add LetsTrust TPM SPI GPIO overlay subpackage for RPi 4.

* Wed Sep 02 2026 Simon de Vlieger <cmdr@supakeen.com> - 2026.10-3.rc3
- Import the disable VBE and SetVariableRT patches from Fedora.

* Wed Sep 02 2026 Simon de Vlieger <cmdr@supakeen.com> - 2026.10-2.rc3
- Import the enable menu patch from Fedora.

* Wed Sep 02 2026 Simon de Vlieger <cmdr@supakeen.com> - 2026.10-0.1.rc3
- Initial package from a clean upstream.
