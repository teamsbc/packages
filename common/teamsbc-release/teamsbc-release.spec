%global dist_version %{fedora}
%define variant_name TeamSBC 

Name:           teamsbc-release
Version:        %{dist_version}
Release:        9
Summary:        TeamSBC release files

License:        MIT

Provides: teamsbc-release = %{version}-%{release}
Provides: teamsbc-release-variant = %{version}-%{release}
Provides: teamsbc-release-identity = %{version}-%{release}

BuildArch:      noarch

Conflicts: system-release

Provides: system-release
Provides: system-release(%version)

Conflicts: fedora-release
Conflicts: fedora-release-identity

Requires: teamsbc-release-common = %{version}-%{release}

Recommends: teamsbc-release-identity-basic

Source10: 90-default.preset
Source11: 99-default-disable.preset

%description
TeamSBC release files

%package common
Summary: TeamSBC release files

Requires: teamsbc-release-variant = %{version}-%{release}
Suggests: teamsbc-release

Requires: teamsbc-release-identity = %{version}-%{release}
Requires: fedora-repos(%{version})
Requires: teamsbc-repos-common

Conflicts: fedora-release-common


%description common
Release files common to all TeamSBC variants

%package identity-basic
Summary:    Package providing the basic TeamSBC identity

RemovePathPostfixes: .basic
Provides:  teamsbc-release-identity = %{version}-%{release}
Conflicts: teamsbc-release-identity

%description identity-basic
Provides the necessary files for a TeamSBC installation that is
not identifying itself as a particular variant.

%package standard
Summary:    Base package for TeamSBC Standard-specific default configurations

RemovePathPostfixes: .standard

Provides:  teamsbc-release = %{version}-%{release}
Provides:  teamsbc-release-variant = %{version}-%{release}
Provides:  system-release
Provides:  system-release(%{version})
Conflicts: fedora-release
Conflicts: fedora-release-identity
Requires:  teamsbc-release-common

Recommends: teamsbc-release-identity-standard

%description standard
Provides a base package for TeamSBC Standard-specific
configuration files to depend on as well as Standard system defaults.

%package identity-standard
Summary:    Package providing the identity for TeamSBC Standard variant

RemovePathPostfixes: .standard
Provides:       teamsbc-release-identity = %{version}-%{release}
Conflicts:      teamsbc-release-identity
Requires(meta): teamsbc-release-standard = %{version}-%{release}

%description identity-standard
Provides the necessary files for a TeamSBC installation that is identifying
itself as TeamSBC Standard.

%package legacy
Summary:    Base package for TeamSBC Standard-specific default configurations

RemovePathPostfixes: .legacy

Provides:  teamsbc-release = %{version}-%{release}
Provides:  teamsbc-release-variant = %{version}-%{release}
Provides:  system-release
Provides:  system-release(%{version})
Conflicts: fedora-release
Conflicts: fedora-release-identity
Requires:  teamsbc-release-common

Recommends: teamsbc-release-identity-legacy

%description legacy
Provides a base package for TeamSBC Legacy-specific
configuration files to depend on as well as Legacy system defaults.

%package identity-legacy
Summary:    Package providing the identity for TeamSBC Legacy variant

RemovePathPostfixes: .legacy
Provides:       teamsbc-release-identity = %{version}-%{release}
Conflicts:      teamsbc-release-identity
Requires(meta): teamsbc-release-legacy = %{version}-%{release}

%description identity-legacy
Provides the necessary files for a TeamSBC installation that is identifying
itself as TeamSBC Legacy.

%prep

%build

%install
install -d %{buildroot}%{_prefix}/lib
echo "TeamSBC release %{version}" > %{buildroot}%{_prefix}/lib/fedora-release
echo "cpe:/o:teamsbc:%{version}" > %{buildroot}%{_prefix}/lib/system-release-cpe

install -d %{buildroot}%{_sysconfdir}
ln -s ../usr/lib/fedora-release %{buildroot}%{_sysconfdir}/fedora-release
ln -s ../usr/lib/system-release-cpe %{buildroot}%{_sysconfdir}/system-release-cpe
ln -s fedora-release %{buildroot}%{_sysconfdir}/redhat-release
ln -s fedora-release %{buildroot}%{_sysconfdir}/system-release

# /etc/os-release
cat <<EOF >os-release
NAME="TeamSBC Linux"
VERSION="%{dist_version} (%{variant_name})"
ID=teamsbc
VERSION_ID=%{dist_version}
VERSION_CODENAME=""
PRETTY_NAME="TeamSBC Linux %{dist_version} (%{variant_name})"
ANSI_COLOR="0;38;2;60;110;180"
LOGO=teamsbc-logo-icon
CPE_NAME="cpe:/o:teamsbc:%{dist_version}"
DEFAULT_HOSTNAME="teamsbc"
HOME_URL="https://teamsbc.org/"
SUPPORT_URL="https://teamsbc.org/"
DOCUMENTATION_URL="https://teamsbc.org/"
BUG_REPORT_URL="https://github.com/teamsbc/distribution/issues"
EOF

# /etc/issue
echo "\S" > %{buildroot}%{_prefix}/lib/issue
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue
echo >> %{buildroot}%{_prefix}/lib/issue
ln -s ../usr/lib/issue %{buildroot}%{_sysconfdir}/issue

# /etc/issue.net
echo "\S" > %{buildroot}%{_prefix}/lib/issue.net
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue.net
ln -s ../usr/lib/issue.net %{buildroot}%{_sysconfdir}/issue.net

# variants
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.basic

cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.standard
echo "VARIANT=\"Standard\"" >> %{buildroot}%{_prefix}/lib/os-release.standard
echo "VARIANT_ID=\"teamsbc-standard\"" >> %{buildroot}%{_prefix}/lib/os-release.standard
sed -i -e "s|(%{variant_name})|(Standard)|g" %{buildroot}%{_prefix}/lib/os-release.standard

cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.legacy
echo "VARIANT=\"Legacy\"" >> %{buildroot}%{_prefix}/lib/os-release.legacy
echo "VARIANT_ID=\"teamsbc-legacy\"" >> %{buildroot}%{_prefix}/lib/os-release.legacy
sed -i -e "s|(%{variant_name})|(Legacy)|g" %{buildroot}%{_prefix}/lib/os-release.legacy

ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release

install -d -m 755 %{buildroot}%{_rpmconfigdir}/macros.d
cat >> %{buildroot}%{_rpmconfigdir}/macros.d/macros.dist << EOF
%%fedora    %{dist_version}
%%dist      %%{?distprefix}.fc%{dist_version}%%{?with_bootstrap:~bootstrap}
%%fc%{dist_version}     1
EOF

# default systemd presets
install -Dm0644 %{SOURCE10} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE11} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/

%files common
%{_prefix}/lib/fedora-release
%{_prefix}/lib/system-release-cpe
%{_sysconfdir}/os-release
%{_sysconfdir}/fedora-release
%{_sysconfdir}/redhat-release
%{_sysconfdir}/system-release
%{_sysconfdir}/system-release-cpe
%attr(0644,root,root) %{_prefix}/lib/issue
%config(noreplace) %{_sysconfdir}/issue
%attr(0644,root,root) %{_prefix}/lib/issue.net
%config(noreplace) %{_sysconfdir}/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir %{_prefix}/lib/systemd/system-preset/
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset

%files
%files identity-basic
%{_prefix}/lib/os-release.basic

%files standard
%files identity-standard
%{_prefix}/lib/os-release.standard

%files legacy
%files identity-legacy
%{_prefix}/lib/os-release.legacy

%changelog
* Sat Feb 29 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-9
- Fix up a last reference to fedoraproject.

* Sat Feb 28 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-8
- Drop usage of "Fedora" without a "Remix" directly attached.

* Fri Feb 27 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-7
- Include legacy variant.

* Fri Feb 13 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-6
- Include systemd presets.

* Sun Feb 08 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-5
- Point bug URL at GitHub.

* Tue Feb 03 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-4
- Remove dependency on `teamsbc-repos-standard` for the standard subpackage.

* Thu Nov 06 2025 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-3
- Dependency on `teamsbc-repos-standard` for the standard subpackage.

* Mon Nov 03 2025 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-2
- Dependency on `teamsbc-repos-common` for the common subpackage.

* Sun Nov 02 2025 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-1
- Initial setup of TeamSBC Fedora Remix's release package.
