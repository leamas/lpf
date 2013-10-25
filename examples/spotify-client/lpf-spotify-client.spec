# %%global will not work here, lazy evaluation needed.
%define         target_pkg %(t=%{name}; echo ${t#lpf-})

Name:           lpf-spotify-client
                # Upstream spotify version, verbatim.
Version:        0.9.4.183.g644e24e.428
Release:        1%{?dist}
Summary:        Spotify music player native client package bootstrap

License:        MIT
URL:            http://leamas.fedorapeople.org/lpf-spotify-client/
Group:          Development/Tools
BuildArch:      noarch
                # There's no source, only a spec building the target package.
Source0:        spotify-client.spec
# http://community.spotify.com/t5/Help-Desktop-Linux-Mac-and/What-license-does-the-linux-spotify-client-use/td-p/173356/highlight/true/page/2
Source1:        eula.txt
Source2:        LICENSE
Source3:        README

BuildRequires:  desktop-file-utils
BuildRequires:  lpf
Requires:       lpf

%description
Bootstrap package allowing the lpf system to build the non-redistributable
spotify-client package.

%prep
%setup -cT
cp %{SOURCE2} LICENSE


%build


%install
# lpf-setup-pkg [eula] <topdir> <specfile> [sources...]
/usr/share/lpf/scripts/lpf-setup-pkg %{SOURCE1} %{buildroot} %{SOURCE0}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%post
lpf scan 2>/dev/null || :

%postun
lpf scan 2>/dev/null || :


%files
%doc LICENSE README
%{_datadir}/applications/%{name}.desktop
%{_datadir}/lpf/packages/%{target_pkg}
%attr(775,pkg-build,pkg-build) /var/lib/lpf/packages/%{target_pkg}
%attr(664,pkg-build,pkg-build) /var/lib/lpf/packages/%{target_pkg}/state


%changelog
* Thu Oct 24 2013 Alec Leamas <leamas@nowhere.net> - 0.9.4.183.g644e24e.428-1
- Updating for  new upstream release.
- Adding LICENSE
- Updating URL:
- Smaller review fixes (layout etc.).
- Adding comment for eula.txt
- Adding README, final review remark fix.

* Sun May 05 2013 Alec Leamas <leamas@nowhere.net> - 0.9.0.133.gd18ed58.259-2
- Initial release
