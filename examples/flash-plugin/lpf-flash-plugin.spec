# %%global will not work here, lazy evaluation needed.
%define         target_pkg %(t=%{name}; echo ${t#lpf-})

Name:           lpf-flash-plugin
Version:        11.2.202.327
Release:        4%{?dist}
Epoch:          1
Summary:        Adobe Flash Player package bootstrap

License:        MIT
URL:            http://github.com/leamas/lpf
Group:          Development/Tools
BuildArch:      noarch
Source0:        flash-plugin.spec.in
Source1:        README
Source2:        LICENSE

BuildRequires:  desktop-file-utils
BuildRequires:  lpf
Requires:       lpf

%description
Bootstrap package allowing the lpf system to build the non-redistributable
flash-plugin package.

The flash-plugin package is available only for i686 and x86_64 systems.

%prep
%setup -cT
cp %{SOURCE1} README
cp %{SOURCE2} LICENSE


%build


%install
# lpf-setup-pkg [-a arch] [-e eula] <topdir> <specfile> [sources...]
/usr/share/lpf/scripts/lpf-setup-pkg %{buildroot} %{SOURCE0}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%post
DISPLAY= lpf scan 2>/dev/null || :

%postun
if [ "$1" = '0' ]; then
    /usr/share/lpf/scripts/lpf-pkg-postun %{target_pkg} &>/dev/null || :
fi

%triggerpostun -- %{target_pkg}
if [ "$2" = '0' ]; then
    lpf scan-removal %{target_pkg} &>/dev/null || :
fi


%files
%doc README LICENSE
/usr/share/applications/%{name}.desktop
/usr/share/lpf/packages/%{target_pkg}
%attr(775,pkg-build,pkg-build) /var/lib/lpf/packages/%{target_pkg}
%attr(664,pkg-build,pkg-build) /var/lib/lpf/packages/%{target_pkg}/state


%changelog
* Wed Nov 27 2013 Simone Caronni <negativo17@gmail.com> - 1:11.2.202.327-4
- Updated postun and triggerpostun sections as per latest specifications.

* Tue Nov 26 2013 Simone Caronni <negativo17@gmail.com> - 1:11.2.202.327-3
- Add triggerpostun section, update description.
- Updated lpf-flash-plugin.spec.in.

* Mon Nov 25 2013 Simone Caronni <negativo17@gmail.com> - 1:11.2.202.327-2
- Updated install, post and postun sections for the latest additions.

* Thu Nov 21 2013 Simone Caronni <negativo17@gmail.com> - 1:11.2.202.327-1
- First build.
