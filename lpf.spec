%global commit 1ef88240c1897f39d80d0f3fe485ce11aeecd013
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           lpf
Version:        0
Release:        2.%{shortcommit}%{?dist}
Summary:        Local package factory - build non-redistributable rpms

                # Icon from iconarchive.com
License:        MIT
URL:            https://github.com/leamas/lpf
Group:          Development/Tools
Source0:        %{url}/archive/%{commit}/lpf-%{version}-%{shortcommit}.tar.gz
BuildArch:      noarch

BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Requires:       rpmdevtools
Requires:       rpm-build
Requires:       sudo
Requires:       zenity
Requires(pre):  shadow-utils


%description
lpf (Local Package Build System) is designed to handle two separate
problems:
 - Packages built from sources which does not allow redistribution.
 - Packages requiring user to accept EULA-like terms.

It works by downloading sources, possibly requiring a user to accept
license terms and then building and installing rpm package(s) locally.
Besides being interactive the operation is similar to akmod and dkms


%prep
%setup -qn lpf-%{commit}


%build


%install
install -m 755 -d %{buildroot}/etc/sudoers.d
install -m 755 -d %{buildroot}/var/lib/lpf/{packages,rpms,approvals,log}
install -m 755 -d %{buildroot}%{_datadir}/lpf/packages
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}%{_libexecdir}

cp -a pkg-build %{buildroot}/etc/sudoers.d
cp -ar scripts examples  %{buildroot}%{_datadir}/lpf
ln -s %{_datadir}/lpf/scripts/lpf %{buildroot}%{_bindir}/lpf

pushd %{buildroot}%{_libexecdir}
ln -s %{_datadir}/lpf/scripts/lpf-kill-pgroup .
popd

for size in 24 32 48 64 128; do
    install -m 644 -D icons/lpf-$size.png \
        %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/lpf.png
done
desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications lpf.desktop


%pre
getent group pkg-build >/dev/null || groupadd -r pkg-build
getent passwd pkg-build >/dev/null || \
    useradd -r -g pkg-build -d /var/lib/lpf -s /bin/bash \
        -c "lpf local package build user" pkg-build
exit 0

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/lpf scan

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc README.md LICENSE
%{_bindir}/lpf
%{_datadir}/lpf
%{_datadir}/applications/lpf.desktop
%{_datadir}/icons/hicolor/*/apps/lpf.png
%{_libexecdir}/lpf-kill-pgroup
%config(noreplace) /etc/sudoers.d/pkg-build
%attr(775, pkg-build, pkg-build)/var/lib/lpf


%changelog
* Sun May 05 2013 Alec Leamas <leamas@nowhere.net> - 0-1.fa1afe1
- Initial release
