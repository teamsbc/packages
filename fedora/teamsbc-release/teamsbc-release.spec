%global dist_version %{fedora}
%define variant_name TeamSBC 

Name:           teamsbc-release
Version:        %{dist_version}
Release:        2
Summary:        Fedora TeamSBC Remix release files

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

%description
Fedora TeamSBC Remix release files

%package common
Summary: Fedora TeamSBC Remix release files

Requires: teamsbc-release-variant = %{version}-%{release}
Suggests: teamsbc-release

Requires: teamsbc-release-identity = %{version}-%{release}
Requires: fedora-repos(%{version})

Conflicts: fedora-release-common

Requires:  teamsbc-repos(%{version})

%description common
Release files common to all Fedora TeamSBC Remix variants

%package identity-basic
Summary:    Package providing the basic Fedora TeamSBC Remix identity

RemovePathPostfixes: .basic
Provides:  teamsbc-release-identity = %{version}-%{release}
Conflicts: teamsbc-release-identity

%description identity-basic
Provides the necessary files for a Fedora TeamSBC Remix installation that is
not identifying itself as a particular variant.

%package standard
Summary:    Base package for Fedora TeamSBC Remix Standard-specific default configurations

RemovePathPostfixes: .standard

Provides: teamsbc-release = %{version}-%{release}
Provides: teamsbc-release-variant = %{version}-%{release}
Provides: system-release
Provides: system-release(%{version})
Conflicts: fedora-release
Conflicts: fedora-release-identity
Requires: teamsbc-release-common

Recommends: teamsbc-release-identity-standard

%description standard
Provides a base package for Fedora TeamSBC Remix Standard-specific
configuration files to depend on as well as Standard system defaults.

%package identity-standard
Summary:    Package providing the identity for Fedora TeamSBC Remix Standard variant

RemovePathPostfixes: .standard
Provides:       teamsbc-release-identity = %{version}-%{release}
Conflicts:      teamsbc-release-identity
Requires(meta): teamsbc-release-standard = %{version}-%{release}

%description identity-standard
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora TeamSBC Remix Standard.

%prep

%build

%install
install -d %{buildroot}%{_prefix}/lib
echo "Fedora release %{version}" > %{buildroot}%{_prefix}/lib/fedora-release
echo "cpe:/o:fedoraproject:fedora:%{version}" > %{buildroot}%{_prefix}/lib/system-release-cpe

install -d %{buildroot}%{_sysconfdir}
ln -s ../usr/lib/fedora-release %{buildroot}%{_sysconfdir}/fedora-release
ln -s ../usr/lib/system-release-cpe %{buildroot}%{_sysconfdir}/system-release-cpe
ln -s fedora-release %{buildroot}%{_sysconfdir}/redhat-release
ln -s fedora-release %{buildroot}%{_sysconfdir}/system-release

# /etc/os-release
cat <<EOF >os-release
NAME="Fedora Linux"
VERSION="%{dist_version} (%{variant_name})"
ID=fedora
VERSION_ID=%{dist_version}
VERSION_CODENAME=""
PRETTY_NAME="Fedora Linux %{dist_version} (%{variant_name})"
ANSI_COLOR="0;38;2;60;110;180"
LOGO=fedora-logo-icon
CPE_NAME="cpe:/o:fedoraproject:fedora:%{dist_version}"
DEFAULT_HOSTNAME="teamsbc"
HOME_URL="https://teamsbc.org/"
SUPPORT_URL="https://teamsbc.org/"
DOCUMENTATION_URL="https://teamsbc.org/"
BUG_REPORT_URL="https://teamsbc.org/"
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
echo "VARIANT=\"TeamSBC Standard\"" >> %{buildroot}%{_prefix}/lib/os-release.standard
echo "VARIANT_ID=\"teamsbc-standard\"" >> %{buildroot}%{_prefix}/lib/os-release.standard
sed -i -e "s|(%{variant_name})|(TeamSBC Standard)|g" %{buildroot}%{_prefix}/lib/os-release.standard

ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release

install -d -m 755 %{buildroot}%{_rpmconfigdir}/macros.d
cat >> %{buildroot}%{_rpmconfigdir}/macros.d/macros.dist << EOF
%%fedora    %{dist_version}
%%dist      %%{?distprefix}.fc%{dist_version}%%{?with_bootstrap:~bootstrap}
%%fc%{dist_version}     1
EOF

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

%files
%files identity-basic
%{_prefix}/lib/os-release.basic

%files standard
%files identity-standard
%{_prefix}/lib/os-release.standard

%changelog
* Mon Nov 03 2025 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-2
- Dependency on `teamsbc-repos` for the common subpackage.

* Sun Nov 02 2025 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-1
- Initial setup of Fedora TeamSBC Remix's release package.
