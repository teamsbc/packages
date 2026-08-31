%global dist_version %{fedora}

Name:           teamsbc-config
Version:        %{dist_version}
Release:        9
Summary:        Fedora TeamSBC Remix package repositories

License:        MIT
BuildRequires:  gnupg2

Provides:       teamsbc-config(%{version}) = %{release}
Requires:       system-release(%{version})

Source1:        00-esp.conf.lhotse
Source2:        50-root.conf.lhotse

Source3:        00-esp.conf.makalu
Source4:        30-usr.conf.makalu
Source5:        31-usr.conf.makalu
Source6:        50-root.conf.makalu
Source7:        20-usr.transfer.makalu
Source8:        RPM-GPG-KEY-teamsbc

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
install -m 644 %{_sourcedir}/31-usr.conf.makalu %{buildroot}%{_prefix}/lib/repart.d/31-usr.conf.makalu
install -m 644 %{_sourcedir}/50-root.conf.makalu %{buildroot}%{_prefix}/lib/repart.d/50-root.conf.makalu

install -d %{buildroot}%{_prefix}/lib/sysupdate.d
install -m 644 %{_sourcedir}/20-usr.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/20-usr.transfer.makalu

install -d %{buildroot}%{_sysconfdir}/systemd
gpg --dearmor < %{_sourcedir}/RPM-GPG-KEY-teamsbc > %{buildroot}%{_sysconfdir}/systemd/import-pubring.pgp
sed -i -e 's/@@DIST_VERSION@@/%{dist_version}/g' \
       -e 's/@@BASEARCH@@/%{_arch}/g' \
       %{buildroot}%{_prefix}/lib/sysupdate.d/20-usr.transfer.makalu

%check

%files common
%dir %{_prefix}/lib/repart.d

%files lhotse
%{_prefix}/lib/repart.d/00-esp.conf.lhotse
%{_prefix}/lib/repart.d/50-root.conf.lhotse

%files makalu
%dir %{_prefix}/lib/sysupdate.d

%{_prefix}/lib/repart.d/00-esp.conf.makalu
%{_prefix}/lib/repart.d/30-usr.conf.makalu
%{_prefix}/lib/repart.d/31-usr.conf.makalu
%{_prefix}/lib/repart.d/50-root.conf.makalu

%{_prefix}/lib/sysupdate.d/20-usr.transfer.makalu
%{_sysconfdir}/systemd/import-pubring.pgp

%post makalu -p <lua>
local image_id = os.getenv("IMAGE_ID")
if image_id then
    local path = rpm.expand("%{_prefix}") .. "/lib/sysupdate.d/20-usr.transfer"
    local f = io.open(path, "r")
    if f then
        local content = f:read("*a")
        f:close()
        content = content:gsub("@@IMAGE_ID@@", image_id)
        f = io.open(path, "w")
        if f then
            f:write(content)
            f:close()
        end
    end
end

%changelog
* Mon Aug 31 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-9
- Install TeamSBC signing key as sysupdate import keyring.

* Sun Aug 30 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-8
- Template IMAGE_ID in sysupdate transfer file via %post Lua scriptlet.

* Sat Aug 29 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-7
- Try out `sysupdate.d` configuration for `makalu`.

* Tue Aug 04 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-6
- Second `usr` partition for `makalu`.

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
