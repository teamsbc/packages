%global dist_version %{fedora}

Name:           teamsbc-config
Version:        %{dist_version}
Release:        17
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
Source9:        10-uki.transfer.makalu
Source10:       30-tmux.transfer.makalu
Source11:       tmux.feature.makalu
Source12:       30-screen.transfer.makalu
Source13:       screen.feature.makalu
Source14:       30-weechat.transfer.makalu
Source15:       weechat.feature.makalu
Source16:       30-usbutils.transfer.makalu
Source17:       usbutils.feature.makalu
Source18:       30-pciutils.transfer.makalu
Source19:       pciutils.feature.makalu
Source20:       30-lsof.transfer.makalu
Source21:       lsof.feature.makalu
Source22:       30-strace.transfer.makalu
Source23:       strace.feature.makalu
Source24:       30-mosquitto.transfer.makalu
Source25:       mosquitto.feature.makalu

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

Provides:  systemd-import-keys
Conflicts: systemd-import-keys

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
install -m 644 %{_sourcedir}/10-uki.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/10-uki.transfer.makalu
install -m 644 %{_sourcedir}/20-usr.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/20-usr.transfer.makalu
install -m 644 %{_sourcedir}/30-tmux.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-tmux.transfer.makalu
install -m 644 %{_sourcedir}/tmux.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/tmux.feature.makalu
install -m 644 %{_sourcedir}/30-screen.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-screen.transfer.makalu
install -m 644 %{_sourcedir}/screen.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/screen.feature.makalu
install -m 644 %{_sourcedir}/30-weechat.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-weechat.transfer.makalu
install -m 644 %{_sourcedir}/weechat.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/weechat.feature.makalu
install -m 644 %{_sourcedir}/30-usbutils.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-usbutils.transfer.makalu
install -m 644 %{_sourcedir}/usbutils.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/usbutils.feature.makalu
install -m 644 %{_sourcedir}/30-pciutils.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-pciutils.transfer.makalu
install -m 644 %{_sourcedir}/pciutils.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/pciutils.feature.makalu
install -m 644 %{_sourcedir}/30-lsof.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-lsof.transfer.makalu
install -m 644 %{_sourcedir}/lsof.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/lsof.feature.makalu
install -m 644 %{_sourcedir}/30-strace.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-strace.transfer.makalu
install -m 644 %{_sourcedir}/strace.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/strace.feature.makalu
install -m 644 %{_sourcedir}/30-mosquitto.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-mosquitto.transfer.makalu
install -m 644 %{_sourcedir}/mosquitto.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/mosquitto.feature.makalu

install -d %{buildroot}%{_prefix}/lib/systemd
gpg --dearmor < %{_sourcedir}/RPM-GPG-KEY-teamsbc > %{buildroot}%{_prefix}/lib/systemd/import-pubring.pgp
sed -i -e 's/@@DIST_VERSION@@/%{dist_version}/g' \
       -e 's/@@BASEARCH@@/%{_arch}/g' \
       %{buildroot}%{_prefix}/lib/sysupdate.d/10-uki.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/20-usr.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-tmux.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-screen.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-weechat.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-usbutils.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-pciutils.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-lsof.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-strace.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-mosquitto.transfer.makalu

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

%{_prefix}/lib/sysupdate.d/10-uki.transfer.makalu
%{_prefix}/lib/sysupdate.d/20-usr.transfer.makalu
%{_prefix}/lib/sysupdate.d/30-tmux.transfer.makalu
%{_prefix}/lib/sysupdate.d/tmux.feature.makalu
%{_prefix}/lib/sysupdate.d/30-screen.transfer.makalu
%{_prefix}/lib/sysupdate.d/screen.feature.makalu
%{_prefix}/lib/sysupdate.d/30-weechat.transfer.makalu
%{_prefix}/lib/sysupdate.d/weechat.feature.makalu
%{_prefix}/lib/sysupdate.d/30-usbutils.transfer.makalu
%{_prefix}/lib/sysupdate.d/usbutils.feature.makalu
%{_prefix}/lib/sysupdate.d/30-pciutils.transfer.makalu
%{_prefix}/lib/sysupdate.d/pciutils.feature.makalu
%{_prefix}/lib/sysupdate.d/30-lsof.transfer.makalu
%{_prefix}/lib/sysupdate.d/lsof.feature.makalu
%{_prefix}/lib/sysupdate.d/30-strace.transfer.makalu
%{_prefix}/lib/sysupdate.d/strace.feature.makalu
%{_prefix}/lib/sysupdate.d/30-mosquitto.transfer.makalu
%{_prefix}/lib/sysupdate.d/mosquitto.feature.makalu
%{_prefix}/lib/systemd/import-pubring.pgp

%post makalu -p <lua>
local image_id = os.getenv("IMAGE_ID")
if image_id then
    local sysupdate_dir = rpm.expand("%{_prefix}") .. "/lib/sysupdate.d/"
    local transfers = {"10-uki.transfer", "20-usr.transfer", "30-tmux.transfer", "30-screen.transfer", "30-weechat.transfer", "30-usbutils.transfer", "30-pciutils.transfer", "30-lsof.transfer", "30-strace.transfer", "30-mosquitto.transfer"}
    for _, name in ipairs(transfers) do
        local path = sysupdate_dir .. name
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
end

%changelog
* Thu Oct 29 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-17
- Ship an optional Mosquitto sysupdate feature and transfer for Makalu.

* Mon Oct 26 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-16
- Ship optional lsof and strace sysupdate features and transfers for Makalu.

* Sun Oct 25 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-15
- Ship optional usbutils and pciutils sysupdate features and transfers for Makalu.

* Fri Oct 23 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-14
- Ship optional screen and weechat sysupdate features and transfers for Makalu.

* Wed Oct 14 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-13
- Ship an optional tmux sysupdate feature and transfer for Makalu.

* Sat Oct 03 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-12
- Ship sysupdate transfer for the UKI alongside the usr partition.

* Sat Sep 26 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-11
- Match update payload filenames prefixed with IMAGE_ID.

* Fri Sep 25 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-10
- Ship signing key in /usr/lib/systemd instead of /etc/systemd now that
  systemd-container splits import-pubring into systemd-import-keys.

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
