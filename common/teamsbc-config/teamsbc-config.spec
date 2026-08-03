%global dist_version %{fedora}

Name:           teamsbc-config
Version:        %{dist_version}
Release:        2
Summary:        Fedora TeamSBC Remix package repositories

License:        MIT

Provides:       teamsbc-config(%{version}) = %{release}
Requires:       system-release(%{version})

BuildArch:      noarch

Source1:        00-esp.conf.standard
Source2:        50-root.conf.standard

Source3:        00-esp.conf.makalu
Source4:        50-root.conf.makalu

Requires:       teamsbc-config-common = %{version}-%{release}

%description
Fedora package repository files for yum and dnf.

%package common
Summary: Fedora TeamSBC Remix common configs.

%description common
Configuration files shared across all TeamSBC variants.

%package standard
Summary: Fedora TeamSBC Remix Standard variant configs.

RemovePathPostfixes: .standard

Provides:  teamsbc-config = %{version}-%{release}
Conflicts: teamsbc-config

Requires: teamsbc-config-common

%description standard
Configuration files specific to the Standard TeamSBC variant.

%package makalu
Summary: Fedora TeamSBC Remix Makalu variant configs.

RemovePathPostfixes: .makalu

Provides:  teamsbc-config = %{version}-%{release}
Conflicts: teamsbc-config

Requires: teamsbc-config-common

%description makalu
Configuration files specific to the Makalu TeamSBC variant.

%prep

%build

%install
install -d %{buildroot}%{_prefix}/lib/repart.d
install -m 644 %{_sourcedir}/00-esp.conf.standard %{buildroot}%{_prefix}/lib/repart.d/00-esp.conf.standard
install -m 644 %{_sourcedir}/50-root.conf.standard %{buildroot}%{_prefix}/lib/repart.d/50-root.conf.standard
install -m 644 %{_sourcedir}/00-esp.conf.makalu %{buildroot}%{_prefix}/lib/repart.d/00-esp.conf.makalu
install -m 644 %{_sourcedir}/50-root.conf.makalu %{buildroot}%{_prefix}/lib/repart.d/50-root.conf.makalu

%check

%files common
%dir %{_prefix}/lib/repart.d

%files standard
%{_prefix}/lib/repart.d/00-esp.conf.standard
%{_prefix}/lib/repart.d/50-root.conf.standard

%files makalu
%{_prefix}/lib/repart.d/00-esp.conf.makalu
%{_prefix}/lib/repart.d/50-root.conf.makalu

%changelog
* Mon Aug 03 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-3
- Include a Makalu subpackage.

* Sun May 31 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-2
- Include an ESP file for systemd-repart.

* Sun May 24 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-1
- Initial setup of TeamSBC Fedora Remix's config package.
