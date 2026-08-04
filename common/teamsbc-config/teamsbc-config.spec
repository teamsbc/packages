%global dist_version %{fedora}

Name:           teamsbc-config
Version:        %{dist_version}
Release:        5
Summary:        Fedora TeamSBC Remix package repositories

License:        MIT

Provides:       teamsbc-config(%{version}) = %{release}
Requires:       system-release(%{version})

BuildArch:      noarch

Source1:        00-esp.conf.lhotse
Source2:        50-root.conf.lhotse

Source3:        00-esp.conf.makalu
Source4:        30-usr.conf.makalu
Source5:        50-root.conf.makalu

Requires:       teamsbc-config-common = %{version}-%{release}

%description
Fedora package repository files for yum and dnf.

%package common
Summary: Fedora TeamSBC Remix common configs.

%description common
Configuration files shared across all TeamSBC variants.

%package lhotse
Summary: Fedora TeamSBC Remix Lhotse variant configs.

RemovePathPostfixes: .lhotse

Provides:  teamsbc-config = %{version}-%{release}
Conflicts: teamsbc-config

Requires: teamsbc-config-common

%description lhotse
Configuration files specific to the Lhotse TeamSBC variant.

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

install -m 644 %{_sourcedir}/00-esp.conf.lhotse %{buildroot}%{_prefix}/lib/repart.d/00-esp.conf.lhotse
install -m 644 %{_sourcedir}/50-root.conf.lhotse %{buildroot}%{_prefix}/lib/repart.d/50-root.conf.lhotse

install -m 644 %{_sourcedir}/00-esp.conf.makalu %{buildroot}%{_prefix}/lib/repart.d/00-esp.conf.makalu
install -m 644 %{_sourcedir}/30-usr.conf.makalu %{buildroot}%{_prefix}/lib/repart.d/30-usr.conf.makalu
install -m 644 %{_sourcedir}/50-root.conf.makalu %{buildroot}%{_prefix}/lib/repart.d/50-root.conf.makalu

%check

%files common
%dir %{_prefix}/lib/repart.d

%files lhotse
%{_prefix}/lib/repart.d/00-esp.conf.lhotse
%{_prefix}/lib/repart.d/50-root.conf.lhotse

%files makalu
%{_prefix}/lib/repart.d/00-esp.conf.makalu
%{_prefix}/lib/repart.d/30-usr.conf.makalu
%{_prefix}/lib/repart.d/50-root.conf.makalu

%changelog
* Tue Aug 04 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-5
- Rename `standard` to `lhotse`.

* Tue Aug 04 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-4
- Rename `standard` to `lhotse`.

* Mon Aug 03 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-3
- Include a Makalu subpackage.

* Sun May 31 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-2
- Include an ESP file for systemd-repart.

* Sun May 24 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-1
- Initial setup of TeamSBC Fedora Remix's config package.
