%global dist_version %{fedora}

Name:           teamsbc-repos
Version:        %{dist_version}
Release:        3
Summary:        Fedora TeamSBC Remix package repositories

License:        MIT

Provides:       teamsbc-repos(%{version}) = %{release}
Requires:       system-release(%{version})

BuildArch:      noarch

Source1:        teamsbc-common.repo
Source2:        teamsbc-standard.repo

Requires:       teamsbc-repos-common = %{version}-%{release}

%description
Fedora package repository files for yum and dnf.

%package common
Summary: Fedora TeamSBC Remix package repositories.

%description common
Fedora package repository files for yum and dnf.

%package standard
Summary:  Fedora TeamSBC Remix package repositories.
Requires: teamsbc-repos-common

%description standard
Fedora package repository files for yum and dnf.

%prep

%build

%install
install -d -m 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -m 644 %{_sourcedir}/teamsbc*repo %{buildroot}%{_sysconfdir}/yum.repos.d

%check

%files common
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/teamsbc-common.repo

%files standard
%config(noreplace) /etc/yum.repos.d/teamsbc-standard.repo

%changelog
* Fri Nov 07 2025 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-3
- Point to new COPR group repositories.

* Thu Nov 06 2025 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-2
- Create `-common` and `-standard` subpackage.

* Mon Nov 03 2025 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-1
- Initial setup of Fedora TeamSBC Remix's package repositories package.
