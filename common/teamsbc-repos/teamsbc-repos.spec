%global dist_version %{fedora}

Name:           teamsbc-repos
Version:        %{dist_version}
Release:        13
Summary:        TeamSBC package repositories

License:        MIT

Provides:       teamsbc-repos(%{version}) = %{release}
Requires:       system-release(%{version})

BuildArch:      noarch

Source1:        teamsbc-common.repo
Source2:        RPM-GPG-KEY-teamsbc

Requires:       teamsbc-repos-common = %{version}-%{release}

%description
TeamSBC package repository files for yum and dnf.

%package common
Summary: TeamSBC package repositories.

%description common
TeamSBC package repository files for yum and dnf.

%prep

%build

%install
install -d -m 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -m 644 %{_sourcedir}/teamsbc*repo %{buildroot}%{_sysconfdir}/yum.repos.d
install -d -m 755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -m 644 %{_sourcedir}/RPM-GPG-KEY-teamsbc %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-teamsbc

%check

%files common
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/teamsbc-common.repo
/etc/pki/rpm-gpg/RPM-GPG-KEY-teamsbc

%changelog
* Fri Aug 07 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-13
- Turn on GPG verification for common repository.

* Fri Aug 07 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-12
- Ship GPG public key for package signature verification.

* Wed Jun 10 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-11
- Set priority on teamsbc repositories.

* Sat May 23 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-10
- Drop usage of Fedora Remix if both words are not together.

* Wed Feb 04 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-9
- Include a latest subdir.

* Tue Feb 03 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-8
- Drop Fedora from repository URL.

* Tue Feb 03 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-7
- Include branch in repository URL.

* Tue Feb 03 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-6
- Slightly prettier repository name.

* Tue Feb 03 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-5
- Actually point to the correct .net domain, not .org.

* Mon Feb 02 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-4
- Point to new packages.teamsbc.net domain.

* Fri Nov 07 2025 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-3
- Point to new COPR group repositories.

* Thu Nov 06 2025 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-2
- Create `-common` and `-standard` subpackage.

* Mon Nov 03 2025 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-1
- Initial setup of Fedora TeamSBC Remix's package repositories package.
