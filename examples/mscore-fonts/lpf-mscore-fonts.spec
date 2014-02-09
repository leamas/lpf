# %%global will not work here, lazy evaluation needed.
%define         target_pkg %(t=%{name}; echo ${t#lpf-})

Name:           lpf-mscore-fonts
Version:        2.2
Release:        1%{?dist}
Summary:        Bootstrap package building mscore-fonts using lpf

License:        MIT
URL:            https://github.com/leamas/lpf
Group:          Development/Tools
BuildArch:      noarch
Source0:        mscore-fonts.spec.in
Source1:        Licen.TXT
Source2:        55-mscore-arial.conf
Source3:        55-mscore-andale.conf
Source4:        55-mscore-comic.conf
Source5:        55-mscore-courier.conf
Source6:        55-mscore-georgia.conf
Source7:        55-mscore-impact.conf
Source8:        55-mscore-times.conf
Source9:        55-mscore-trebuchet.conf
Source10:       55-mscore-verdana.conf
Source11:       55-mscore-webdings.conf

BuildRequires:  desktop-file-utils
BuildRequires:  lpf
Requires:       lpf


%description
Bootstrap package allowing the lpf system to build the
mscore-fonts non-redistributable package.


%prep
%setup -cT


%build


%install
# lpf-setup-pkg [-e eula] <topdir> <specfile> [sources...]
/usr/share/lpf/scripts/lpf-setup-pkg -e %{SOURCE1} %{buildroot} %{SOURCE0} \
    %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} \
    %{SOURCE7} %{SOURCE8} %{SOURCE9} %{SOURCE10} %{SOURCE11}


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
* Mon Feb 10 2014 Alec Leamas <leamas.alec@gmail.com> - 2.2-1
- Initial release
