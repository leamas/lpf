# %%global will not work here, lazy evaluation needed.
%define         target_pkg %(t=%{name}; echo ${t#lpf-})

Name:           lpf-spotify-client
Version:        0.9.0.133.gd18ed58.259
Release:        1%{?dist}
Summary:        Spotify music player native client package bootstrap

License:        MIT
URL:            http://leamas.fedorapeople.org/spotify/0.9.0/%{name}.spec
Group:          Development/Tools
BuildArch:      noarch
Source0:        spotify-client.spec
Source1:        eula.txt

BuildRequires:  desktop-file-utils
BuildRequires:  lpf
Requires:       lpf

%description
Bootstrap package allowing the lpf system to build the
non-redistributable spotify-client package.

%prep
%setup -cT


%build


%install
# lpf-setup-pkg [eula] <topdir> <specfile> [sources...]
/usr/share/lpf/scripts/lpf-setup-pkg \
    %{SOURCE1} %{buildroot} %{SOURCE0}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%post
lpf scan 2>/dev/null || :

%postun
lpf scan 2>/dev/null || :


%files
%{_datadir}/applications/%{name}.desktop
%{_datadir}/lpf/packages/%{target_pkg}
%attr(775,pkg-build,pkg-build) /var/lib/lpf/packages/%{target_pkg}
%attr(664,pkg-build,pkg-build) /var/lib/lpf/packages/%{target_pkg}/state


%changelog
* Sun May 05 2013 Alec Leamas <leamas@nowhere.net> - 0.9.0.133.gd18ed58.259-2
- Initial release
