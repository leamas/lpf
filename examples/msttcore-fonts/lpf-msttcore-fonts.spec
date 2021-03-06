# %%global will not work here, lazy evaluation needed.
%define         target_pkg %(t=%{name}; echo ${t#lpf-})

Name:           lpf-msttcore-fonts
Version:        2.2
Release:        1%{?dist}
Summary:        Bootstrap package building msttcore-fonts using lpf

License:        MIT
URL:            https://github.com/leamas/lpf
Group:          Development/Tools
BuildArch:      noarch
Source0:        msttcore-fonts.spec.in
BuildRequires:  desktop-file-utils
BuildRequires:  lpf
Requires:       lpf
Requires:       lpf-mscore-fonts
Requires:       lpf-mscore2-fonts


%description
Bootstrap package allowing the lpf system to build the
msttccore-fonts non-redistributable package.


%prep
%setup -cT


%build


%install
# lpf-setup-pkg [eula] <topdir> <specfile> [sources...]
/usr/share/lpf/scripts/lpf-setup-pkg %{buildroot} %{SOURCE0}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%post
%lpf_post

%postun
%lpf_postun

%lpf_triggerpostun


%files
%{_datadir}/applications/%{name}.desktop
%{_datadir}/lpf/packages/%{target_pkg}
%attr(775,pkg-build,pkg-build) /var/lib/lpf/packages/%{target_pkg}


%changelog
* Sun May 05 2013 Alec Leamas <leamas@nowhere.net> - 0.9.0.133.gd18ed58.259-2
- Initial release
