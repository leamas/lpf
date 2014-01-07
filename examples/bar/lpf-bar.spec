# Nothing to strip -> no debug package (non-arch files in arch pkg).
%global         __strip /bin/true
%global         debug_package %{nil}

# %%global will not work here, lazy evaluation needed.
%define         target_pkg %(t=%{name}; echo ${t#lpf-})

Name:           lpf-bar
                # Upstream spotify version, verbatim.
Version:        1.0
Release:        1%{?dist}
Summary:        Bar non-redistributable app.

License:        MIT
URL:            https://github.com/leamas/lpf
Group:          Development/Tools
BuildArch:      noarch
                # There's no source, only a spec building the target package.
Source0:        bar.spec.in
Source1:        eula.txt
Source2:        README.fedora
Source3:        bar.sh
Source4:        README

BuildRequires:  desktop-file-utils
BuildRequires:  lpf
Requires:       lpf

%description
Bootstrap package allowing the lpf system to build the non-redistributable
bar package.


%prep
%setup -cT
cp -a %{SOURCE4} README


%build


%install
# lpf-setup-pkg [-a arch] [-e eula] <topdir> <specfile> [sources...]
/usr/share/lpf/scripts/lpf-setup-pkg -e %{SOURCE1} %{buildroot} %{SOURCE0} \
    %{SOURCE2} %{SOURCE3}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%post
%lpf_post

%postun
%lpf_postun

%lpf_triggerpostun


%files
%doc README
%{_datadir}/applications/%{name}.desktop
%{_datadir}/lpf/packages/%{target_pkg}
%dir %attr(775,pkg-build,pkg-build) /var/lib/lpf/packages/%{target_pkg}
%attr(664,pkg-build,pkg-build) /var/lib/lpf/packages/%{target_pkg}/state


%changelog
* Thu Oct 24 2013 Alec Leamas <leamas@nowhere.net> - 1.0-1
- Updating for  new upstream release.
