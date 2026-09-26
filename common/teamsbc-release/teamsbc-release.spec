%global dist_version %{fedora}
%define variant_name TeamSBC 

Name:           teamsbc-release
Version:        %{dist_version}
Release:        31
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

%package lhotse
Summary:    Base package for TeamSBC Lhotse-specific default configurations

RemovePathPostfixes: .lhotse

Provides:  teamsbc-release = %{version}-%{release}
Provides:  teamsbc-release-variant = %{version}-%{release}
Provides:  system-release
Provides:  system-release(%{version})
Conflicts: fedora-release
Conflicts: fedora-release-identity
Requires:  teamsbc-release-common

# We configure DNF so the location must exist
Requires:  libdnf5

Recommends: teamsbc-release-identity-lhotse

%description lhotse
Provides a base package for TeamSBC Lhotse-specific
configuration files to depend on as well as Lhotse system defaults.

%package identity-lhotse
Summary:    Package providing the identity for TeamSBC Lhotse variant

RemovePathPostfixes: .lhotse
Provides:       teamsbc-release-identity = %{version}-%{release}
Conflicts:      teamsbc-release-identity
Requires(meta): teamsbc-release-lhotse = %{version}-%{release}

%description identity-lhotse
Provides the necessary files for a TeamSBC installation that is identifying
itself as TeamSBC Lhotse.

%package makalu
Summary:    Base package for TeamSBC Makalu-specific default configurations

RemovePathPostfixes: .makalu

Provides:  teamsbc-release = %{version}-%{release}
Provides:  teamsbc-release-variant = %{version}-%{release}
Provides:  system-release
Provides:  system-release(%{version})
Conflicts: fedora-release
Conflicts: fedora-release-identity
Requires:  teamsbc-release-common

Recommends: teamsbc-release-identity-makalu

%description makalu
Provides a base package for TeamSBC Makalu-specific
configuration files to depend on as well as Makalu system defaults.

%package identity-makalu
Summary:    Package providing the identity for TeamSBC Makalu variant

RemovePathPostfixes: .makalu
Provides:       teamsbc-release-identity = %{version}-%{release}
Conflicts:      teamsbc-release-identity
Requires(meta): teamsbc-release-makalu = %{version}-%{release}

%description identity-makalu
Provides the necessary files for a TeamSBC installation that is identifying
itself as TeamSBC Makalu.

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

install -d %{buildroot}%{_prefix}/lib/kernel
install -d %{buildroot}%{_sysconfdir}/kernel
echo "3" > %{buildroot}%{_sysconfdir}/kernel/tries

install -d %{buildroot}%{_prefix}/lib/kernel/install.conf.d
echo "layout=bls" > %{buildroot}%{_prefix}/lib/kernel/install.conf.d/20-teamsbc.conf.lhotse
echo "entry_name_format=%%M_%%v" >> %{buildroot}%{_prefix}/lib/kernel/install.conf.d/20-teamsbc.conf.lhotse
echo "" > %{buildroot}%{_prefix}/lib/kernel/cmdline.lhotse

echo "layout=uki" > %{buildroot}%{_prefix}/lib/kernel/install.conf.d/20-teamsbc.conf.makalu
echo "entry_name_format=%%M_%%A" >> %{buildroot}%{_prefix}/lib/kernel/install.conf.d/20-teamsbc.conf.makalu
echo "initrd_generator=dracut" >> %{buildroot}%{_prefix}/lib/kernel/install.conf.d/20-teamsbc.conf.makalu
echo "uki_generator=ukify" >> %{buildroot}%{_prefix}/lib/kernel/install.conf.d/20-teamsbc.conf.makalu
echo "mount.usr=dissect" > %{buildroot}%{_prefix}/lib/kernel/cmdline.makalu

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
      %{buildroot}%{_prefix}/lib/os-release.lhotse
echo "VARIANT=\"Lhotse\"" >> %{buildroot}%{_prefix}/lib/os-release.lhotse
echo "VARIANT_ID=\"teamsbc-lhotse\"" >> %{buildroot}%{_prefix}/lib/os-release.lhotse
sed -i -e "s|(%{variant_name})|(Lhotse)|g" %{buildroot}%{_prefix}/lib/os-release.lhotse

cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.makalu
echo "VARIANT=\"Makalu\"" >> %{buildroot}%{_prefix}/lib/os-release.makalu
echo "VARIANT_ID=\"teamsbc-makalu\"" >> %{buildroot}%{_prefix}/lib/os-release.makalu
sed -i -e "s|(%{variant_name})|(Makalu)|g" %{buildroot}%{_prefix}/lib/os-release.makalu

ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release

install -d -m 755 %{buildroot}%{_rpmconfigdir}/macros.d
cat >> %{buildroot}%{_rpmconfigdir}/macros.d/macros.dist << EOF
%%fedora    %{dist_version}
%%dist      %%{?distprefix}.fc%{dist_version}%%{?with_bootstrap:~bootstrap}
%%fc%{dist_version}     1
EOF

install -d -m 755 %{buildroot}%{_datadir}/dnf5/libdnf.conf.d
cat >> %{buildroot}%{_datadir}/dnf5/libdnf.conf.d/20-exclude-bcm283x.conf << EOF
[main]
exclude=bcm283x-firmware
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
%dir %{_prefix}/lib/kernel
%dir %{_prefix}/lib/kernel/install.conf.d
%{_sysconfdir}/kernel/tries
%ghost %{_prefix}/lib/kernel/entry-token
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

%files lhotse
%files identity-lhotse
%{_prefix}/lib/os-release.lhotse
%{_prefix}/lib/kernel/install.conf.d/20-teamsbc.conf.lhotse
%{_prefix}/lib/kernel/cmdline.lhotse
%{_datadir}/dnf5/libdnf.conf.d/20-exclude-bcm283x.conf

%files makalu
%files identity-makalu
%{_prefix}/lib/os-release.makalu
%{_prefix}/lib/kernel/install.conf.d/20-teamsbc.conf.makalu
%{_prefix}/lib/kernel/cmdline.makalu

%post common -p <lua>
local image_id = os.getenv("IMAGE_ID")
if not image_id or image_id == "" then
    image_id = "teamsbc"
end
local path = rpm.expand("%{_prefix}") .. "/lib/kernel/entry-token"
local f = io.open(path, "w")
if f then
    f:write(image_id .. "\n")
    f:close()
end

%post -n %{name}-identity-lhotse -p <lua>
local image_id = os.getenv("IMAGE_ID")
if image_id then
    local path = rpm.expand("%{_prefix}") .. "/lib/os-release"
    local f = io.open(path, "a")
    if f then
        f:write('IMAGE_ID="' .. image_id .. '"\n')
        f:close()
    end
end

%post -n %{name}-identity-makalu -p <lua>
local image_id = os.getenv("IMAGE_ID")
local image_version = os.getenv("IMAGE_VERSION")
if image_id or image_version then
    local path = rpm.expand("%{_prefix}") .. "/lib/os-release"
    local f = io.open(path, "a")
    if f then
        if image_id then
            f:write('IMAGE_ID="' .. image_id .. '"\n')
        end
        if image_version then
            f:write('IMAGE_VERSION="' .. image_version .. '"\n')
        end
        f:close()
    end
end

%changelog
* Sat Sep 26 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-31
- Move kernel config (entry-token, tries, install.conf, cmdline) from
  /etc/kernel to /usr/lib/kernel and DNF vendor config to
  /usr/share/dnf5/libdnf.conf.d so we no longer ship files in /etc
  beyond the conventional symlinks. entry-token is now written
  dynamically in %%post using IMAGE_ID (falling back to "teamsbc").
  Include IMAGE_ID in both entry_name_formats (%%M_%%v for Lhotse,
  %%M_%%A for Makalu).

* Sat Sep 26 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-30
- Simplify the `entry_name_format` to just the relevant version, we'll be
  setting the `entry_token` itself in the future to keep various things
  apart.

* Sat Sep 26 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-29
- Also write `IMAGE_ID` for the Lhotse variant. We tend to only set the
  `IMAGE_ID` here and that does get used by the entry names. `IMAGE_VERSION`
  does not make sense in this context.

* Sat Sep 26 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-28
- Configure boot entry names using the kernel version for Lhotse and the
  image version for Makalu, including the entry token, image ID, and architecture.

* Fri Aug 7 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-27
- Convert identity-makalu %%post to Lua scriptlet to avoid /bin/sh
  dependency ordering issues.

* Fri Aug 7 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-26
- Require(post) /bin/sh to ensure ordering correctness.

* Fri Aug 7 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-25
- Move the post-write to identity since it's what owns the file.

* Thu Aug 6 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-24
- Support writing additional bits to os-release depending on
  environment.

* Tue Aug 4 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-23
- Rename `standard` to `lhotse`.

* Mon Aug 3 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-22
- Enable `mount.usr=dissect` only for Makalu.

* Mon Aug 3 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-21
- Revert `mount.usr=dissect` as it times out trying to find /usr.

* Mon Aug 3 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-20
- Revert `root=dissect` as `dracut` cannot handle it.

* Mon Aug 3 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-19
- Set our default cmdline to dissect.

* Mon Aug 3 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-18
- Further configure Makalu's kernel-install. When the layout is set to
  UKI and the UKI generator is not set dracut builds an uki.efi so it
  tries to build the entire UKI itself instead of just building an
  initrd that 60-ukify can then use.

* Mon Aug 3 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-17
- Ship a kernel cmdline.

* Mon Aug 3 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-16
- Create a Makalu variant.

* Mon Aug 3 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-15
- Move kernel/install.conf to variant-specific package.

* Tue Jun 16 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-14
- Turn on boot counting.

* Tue Jun 16 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-13
- Exclude bcm283x-firmware on standard variant.

* Sat May 16 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-12
- Drop legacy variant.

* Tue Apr 21 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-11
- Create /etc/kernel/install.conf

* Tue Apr 21 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-10
- Create /etc/kernel/entry-token

* Sat Feb 28 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-9
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
