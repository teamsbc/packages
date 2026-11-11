%global dist_version %{fedora}

Name:           teamsbc-config
Version:        %{dist_version}
Release:        23
Summary:        Fedora TeamSBC Remix package repositories

License:        MIT
BuildRequires:  gnupg2

Provides:       teamsbc-config(%{version}) = %{release}
Requires:       system-release(%{version})

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
Source26:       30-copyparty.transfer.makalu
Source27:       copyparty.feature.makalu
Source28:       30-haproxy.transfer.makalu
Source29:       haproxy.feature.makalu
Source30:       30-lm-sensors.transfer.makalu
Source31:       lm-sensors.feature.makalu
Source32:       30-jq.transfer.makalu
Source33:       jq.feature.makalu
Source34:       30-tcpdump.transfer.makalu
Source35:       tcpdump.feature.makalu
Source36:       30-htop.transfer.makalu
Source37:       htop.feature.makalu
Source38:       30-iperf3.transfer.makalu
Source39:       iperf3.feature.makalu
Source40:       30-ethtool.transfer.makalu
Source41:       ethtool.feature.makalu
Source42:       30-smartmontools.transfer.makalu
Source43:       smartmontools.feature.makalu
Source44:       30-nvme-cli.transfer.makalu
Source45:       nvme-cli.feature.makalu
Source46:       30-bind-utils.transfer.makalu
Source47:       bind-utils.feature.makalu
Source48:       30-ripgrep.transfer.makalu
Source49:       ripgrep.feature.makalu
Source50:       30-nmap.transfer.makalu
Source51:       nmap.feature.makalu
Source52:       30-fio.transfer.makalu
Source53:       fio.feature.makalu
Source54:       30-i2c-tools.transfer.makalu
Source55:       i2c-tools.feature.makalu
Source56:       30-bpftrace.transfer.makalu
Source57:       bpftrace.feature.makalu
Source58:       30-i2c-display.transfer.makalu
Source59:       i2c-display.feature.makalu
Source60:       30-podman.transfer.makalu
Source61:       podman.feature.makalu
Source62:       30-valkey.transfer.makalu
Source63:       valkey.feature.makalu

Requires:       teamsbc-config-common = %{version}-%{release}

%description
Fedora package repository files for yum and dnf.

%package common
Summary: Fedora TeamSBC Remix common configs.

%description common
Configuration files shared across all TeamSBC variants.

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
install -m 644 %{_sourcedir}/30-copyparty.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-copyparty.transfer.makalu
install -m 644 %{_sourcedir}/copyparty.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/copyparty.feature.makalu
install -m 644 %{_sourcedir}/30-haproxy.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-haproxy.transfer.makalu
install -m 644 %{_sourcedir}/haproxy.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/haproxy.feature.makalu
install -m 644 %{_sourcedir}/30-lm-sensors.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-lm-sensors.transfer.makalu
install -m 644 %{_sourcedir}/lm-sensors.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/lm-sensors.feature.makalu
install -m 644 %{_sourcedir}/30-jq.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-jq.transfer.makalu
install -m 644 %{_sourcedir}/jq.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/jq.feature.makalu
install -m 644 %{_sourcedir}/30-tcpdump.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-tcpdump.transfer.makalu
install -m 644 %{_sourcedir}/tcpdump.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/tcpdump.feature.makalu
install -m 644 %{_sourcedir}/30-htop.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-htop.transfer.makalu
install -m 644 %{_sourcedir}/htop.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/htop.feature.makalu
install -m 644 %{_sourcedir}/30-iperf3.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-iperf3.transfer.makalu
install -m 644 %{_sourcedir}/iperf3.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/iperf3.feature.makalu
install -m 644 %{_sourcedir}/30-ethtool.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-ethtool.transfer.makalu
install -m 644 %{_sourcedir}/ethtool.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/ethtool.feature.makalu
install -m 644 %{_sourcedir}/30-smartmontools.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-smartmontools.transfer.makalu
install -m 644 %{_sourcedir}/smartmontools.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/smartmontools.feature.makalu
install -m 644 %{_sourcedir}/30-nvme-cli.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-nvme-cli.transfer.makalu
install -m 644 %{_sourcedir}/nvme-cli.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/nvme-cli.feature.makalu
install -m 644 %{_sourcedir}/30-bind-utils.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-bind-utils.transfer.makalu
install -m 644 %{_sourcedir}/bind-utils.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/bind-utils.feature.makalu
install -m 644 %{_sourcedir}/30-ripgrep.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-ripgrep.transfer.makalu
install -m 644 %{_sourcedir}/ripgrep.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/ripgrep.feature.makalu
install -m 644 %{_sourcedir}/30-nmap.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-nmap.transfer.makalu
install -m 644 %{_sourcedir}/nmap.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/nmap.feature.makalu
install -m 644 %{_sourcedir}/30-fio.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-fio.transfer.makalu
install -m 644 %{_sourcedir}/fio.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/fio.feature.makalu
install -m 644 %{_sourcedir}/30-i2c-tools.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-i2c-tools.transfer.makalu
install -m 644 %{_sourcedir}/i2c-tools.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/i2c-tools.feature.makalu
install -m 644 %{_sourcedir}/30-bpftrace.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-bpftrace.transfer.makalu
install -m 644 %{_sourcedir}/bpftrace.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/bpftrace.feature.makalu
install -m 644 %{_sourcedir}/30-i2c-display.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-i2c-display.transfer.makalu
install -m 644 %{_sourcedir}/i2c-display.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/i2c-display.feature.makalu
install -m 644 %{_sourcedir}/30-podman.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-podman.transfer.makalu
install -m 644 %{_sourcedir}/podman.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/podman.feature.makalu
install -m 644 %{_sourcedir}/30-valkey.transfer.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/30-valkey.transfer.makalu
install -m 644 %{_sourcedir}/valkey.feature.makalu %{buildroot}%{_prefix}/lib/sysupdate.d/valkey.feature.makalu

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
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-mosquitto.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-copyparty.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-haproxy.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-lm-sensors.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-jq.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-tcpdump.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-htop.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-iperf3.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-ethtool.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-smartmontools.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-nvme-cli.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-bind-utils.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-ripgrep.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-nmap.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-fio.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-i2c-tools.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-bpftrace.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-i2c-display.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-podman.transfer.makalu \
       %{buildroot}%{_prefix}/lib/sysupdate.d/30-valkey.transfer.makalu

%check

%files common
%dir %{_prefix}/lib/repart.d

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
%{_prefix}/lib/sysupdate.d/30-copyparty.transfer.makalu
%{_prefix}/lib/sysupdate.d/copyparty.feature.makalu
%{_prefix}/lib/sysupdate.d/30-haproxy.transfer.makalu
%{_prefix}/lib/sysupdate.d/haproxy.feature.makalu
%{_prefix}/lib/sysupdate.d/30-lm-sensors.transfer.makalu
%{_prefix}/lib/sysupdate.d/lm-sensors.feature.makalu
%{_prefix}/lib/sysupdate.d/30-jq.transfer.makalu
%{_prefix}/lib/sysupdate.d/jq.feature.makalu
%{_prefix}/lib/sysupdate.d/30-tcpdump.transfer.makalu
%{_prefix}/lib/sysupdate.d/tcpdump.feature.makalu
%{_prefix}/lib/sysupdate.d/30-htop.transfer.makalu
%{_prefix}/lib/sysupdate.d/htop.feature.makalu
%{_prefix}/lib/sysupdate.d/30-iperf3.transfer.makalu
%{_prefix}/lib/sysupdate.d/iperf3.feature.makalu
%{_prefix}/lib/sysupdate.d/30-ethtool.transfer.makalu
%{_prefix}/lib/sysupdate.d/ethtool.feature.makalu
%{_prefix}/lib/sysupdate.d/30-smartmontools.transfer.makalu
%{_prefix}/lib/sysupdate.d/smartmontools.feature.makalu
%{_prefix}/lib/sysupdate.d/30-nvme-cli.transfer.makalu
%{_prefix}/lib/sysupdate.d/nvme-cli.feature.makalu
%{_prefix}/lib/sysupdate.d/30-bind-utils.transfer.makalu
%{_prefix}/lib/sysupdate.d/bind-utils.feature.makalu
%{_prefix}/lib/sysupdate.d/30-ripgrep.transfer.makalu
%{_prefix}/lib/sysupdate.d/ripgrep.feature.makalu
%{_prefix}/lib/sysupdate.d/30-nmap.transfer.makalu
%{_prefix}/lib/sysupdate.d/nmap.feature.makalu
%{_prefix}/lib/sysupdate.d/30-fio.transfer.makalu
%{_prefix}/lib/sysupdate.d/fio.feature.makalu
%{_prefix}/lib/sysupdate.d/30-i2c-tools.transfer.makalu
%{_prefix}/lib/sysupdate.d/i2c-tools.feature.makalu
%{_prefix}/lib/sysupdate.d/30-bpftrace.transfer.makalu
%{_prefix}/lib/sysupdate.d/bpftrace.feature.makalu
%{_prefix}/lib/sysupdate.d/30-i2c-display.transfer.makalu
%{_prefix}/lib/sysupdate.d/i2c-display.feature.makalu
%{_prefix}/lib/sysupdate.d/30-podman.transfer.makalu
%{_prefix}/lib/sysupdate.d/podman.feature.makalu
%{_prefix}/lib/sysupdate.d/30-valkey.transfer.makalu
%{_prefix}/lib/sysupdate.d/valkey.feature.makalu
%{_prefix}/lib/systemd/import-pubring.pgp

%post makalu -p <lua>
local image_id = os.getenv("IMAGE_ID")
if image_id then
    local sysupdate_dir = rpm.expand("%{_prefix}") .. "/lib/sysupdate.d/"
    local transfers = {"10-uki.transfer", "20-usr.transfer", "30-tmux.transfer", "30-screen.transfer", "30-weechat.transfer", "30-usbutils.transfer", "30-pciutils.transfer", "30-lsof.transfer", "30-strace.transfer", "30-mosquitto.transfer", "30-copyparty.transfer", "30-haproxy.transfer", "30-lm-sensors.transfer", "30-jq.transfer", "30-tcpdump.transfer", "30-htop.transfer", "30-iperf3.transfer", "30-ethtool.transfer", "30-smartmontools.transfer", "30-nvme-cli.transfer", "30-bind-utils.transfer", "30-ripgrep.transfer", "30-nmap.transfer", "30-fio.transfer", "30-i2c-tools.transfer", "30-bpftrace.transfer", "30-i2c-display.transfer", "30-podman.transfer", "30-valkey.transfer"}
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
* Wed Nov 11 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-23
- Drop the Lhotse variant.

* Mon Nov 09 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-22
- Add optional Podman and Valkey system extensions for Makalu.

* Wed Nov 04 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-21
- Add optional Makalu utilities and i2c-display system extensions.

* Tue Nov 03 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-20
- Rename the lm-sensors sysupdate feature to match its extension image.

* Sat Oct 31 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-19
- Ship an optional lm_sensors sysupdate feature and transfer for Makalu.

* Sat Oct 31 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-18
- Ship optional copyparty and HAProxy sysupdate features and transfers for Makalu.

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
