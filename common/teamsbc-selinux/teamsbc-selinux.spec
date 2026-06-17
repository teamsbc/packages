%global dist_version %{fedora}

%global selinuxtype targeted
%global modulename teamsbc

Name:           teamsbc-selinux
Version:        %{dist_version}
Release:        1
Summary:        TeamSBC SELinux policies 

License:        MIT

Source2:        %{modulename}.te
Source3:        %{modulename}.fc

Provides:       teamsbc-selinux(%{version}) = %{release}

BuildArch:      noarch

Requires:       selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}

BuildRequires:  selinux-policy-devel
%{?selinux_requires_min}

%description
TeamSBC SELinux policy files.

%prep

%build
mkdir selinux
cp -p %{SOURCE2} ./
cp -p %{SOURCE3} ./

make -f /usr/share/selinux/devel/Makefile %{modulename}.pp
bzip2 -9 %{modulename}.pp

%pre
%selinux_relabel_pre -s %{selinuxtype}

%install
install -D -m 0644 %{modulename}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2

%check

%files
%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2

%posttrans
%selinux_relabel_post -s %{selinuxtype}

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
fi

%changelog
* Wed Jun 17 2026 Simon de Vlieger <cmdr@supakeen.com> - %{fedora}-1
- Set priority on teamsbc repositories.
