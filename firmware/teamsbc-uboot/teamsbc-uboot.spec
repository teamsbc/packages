%global candidate rc3
%global uboot_version %{version}%{?candidate:-%{candidate}}
# No ELF binaries, only firmware blobs; disable empty debuginfo/debugsource packages
%global debug_package %{nil}

Name:     teamsbc-uboot
Version:  2026.10
Release:  0.1%{?candidate:.%{candidate}}%{?dist}
Summary:  U-Boot firmware images for TeamSBC
License:  GPL-2.0-or-later AND LicenseRef-Callaway-BSD AND LGPL-2.1-or-later AND LGPL-2.0-or-later
URL:      https://u-boot-project.org/
ExclusiveArch: aarch64

Source0:  https://git.u-boot-project.org/u-boot/u-boot/-/archive/v%{uboot_version}/u-boot-v%{uboot_version}.tar.bz2

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

%package rpi5
Summary:  U-Boot firmware for Raspberry Pi 5
BuildArch: noarch

%description rpi5
U-Boot firmware image for Raspberry Pi 5.

%prep
%autosetup -n u-boot-v%{uboot_version}

%build
# Both RPi 4 and RPi 5 use the unified rpi_arm64 defconfig
mkdir -p builds/rpi_arm64
make rpi_arm64_defconfig O=builds/rpi_arm64/
%make_build HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" O=builds/rpi_arm64/

%install
for board in rpi4 rpi5; do
  install -pDm 0644 builds/rpi_arm64/u-boot.bin \
    %{buildroot}%{_datadir}/%{name}/${board}/u-boot.bin
done

%files rpi4
%license Licenses/gpl-2.0.txt
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/rpi4/

%files rpi5
%license Licenses/gpl-2.0.txt
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/rpi5/

%changelog
* Wed Sep 02 2026 Simon de Vlieger <cmdr@supakeen.com> - 2026.10-0.1.rc3
- Initial package from a clean upstream.
