%global dist_version %{fedora}

Name:           teamsbc-config
Version:        %{dist_version}
Release:        1
Summary:        Fedora TeamSBC Remix package repositories

License:        MIT

Provides:       teamsbc-config(%{version}) = %{release}
Requires:       system-release(%{version})

BuildArch:      noarch

Source1:        50-root.conf.standard

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

%prep

%build

%install
install -d %{buildroot}%{_prefix}/lib/repart.d
install -m 644 %{_sourcedir}/50-root.conf.standard %{buildroot}%{_prefix}/lib/repart.d/50-root.conf.standard

%check

%files common
%dir %{_prefix}/lib/repart.d

%files standard
%{_prefix}/lib/repart.d/50-root.conf.standard

%changelog
* Sun May 24 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-1
- Initial setup of TeamSBC Fedora Remix's config package.
