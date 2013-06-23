#
# Example lpf-package spec file
#
# This example is for a hypothetic package containing a
# non-redistributable font called called restricted-fonts.
#
# Prerequisites:
# - The target package spec file i. e., restricted-fonts.spec.
# - If the target package needs user to confirm some eula-kind
#   terms the file with these terms, here called eula.txt
# - Any sources or patches the target package uses which does not
#   have a download link in their Source: or Patch: tags (i. e.,
#   any source or patch which spectool -g can't download).

# %%global will not work here, lazy evaluation needed.
%define         target_pkg %(t=%{name}; echo ${t#lpf-})

# The lpf package has the name lpf-<target-package>.spec:
Name:           lpf-restricted-fonts
# The lpf package version is the same as the target package:
Version:        2.2
Release:        1%{?dist}
Summary:        Bootstrap package building restricted-fonts using lpf

# The license and url of the lpf package are basically void:
License:        MIT
URL:            https://github.com/leamas/lpf
Group:          Development/Tools
BuildArch:      noarch
# The target package spec:
Source0:        restricted-fonts.spec
# The terms user needs to accept before building package.
Source1:        eula.txt
# Add sources and patches used by target spec which can't
# be downloaded:
Source2:        restricted-fonts-fontconfig.conf

BuildRequires:  desktop-file-utils
BuildRequires:  lpf
Requires:       lpf


%description
Bootstrap package allowing the lpf system to build the
restricted-fonts non-redistributable package.


%prep
%setup -cT
rm -rf examples


%build


%install
# lpf-setup-pkg creates the package structure according to:
# lpf-setup-pkg [eula] <topdir> <specfile> [sources...]:
/usr/share/lpf/scripts/lpf-setup-pkg \
    %{SOURCE1} %{buildroot} %{SOURCE0} %{SOURCE2}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


# Remaining parts should not need any editing besides the changelog:
%post
lpf scan %{target_pkg} &>/dev/null || :

%triggerpostun -- %{target_pkg}
lpf scan-removal %{target_pkg} &>/dev/null || :

%triggerin -- %{target_pkg}
lpf scan %{target_pkg} &>/dev/null || :


%files
%{_datadir}/applications/%{name}.desktop
%{_datadir}/lpf/packages/%{target_pkg}
%attr(775,pkg-build,pkg-build) /var/lib/lpf/packages/%{target_pkg}


%changelog
* Sun May 05 2013 Alec Leamas <leamas@nowhere.net> - 0.9.0.133.gd18ed58.259-2
- Initial release
