#These refer to the installer, not the main package:
%global commit      cb564f2c83b93055ad94564f8df04f74fe88af9a
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global repo        http://repository.spotify.com/pool/non-free/s/spotify
%global github_repo https://github.com/leamas/spotify-make/archive/%{commit}

# We cannot strip this binary (licensing restrictions).
%global debug_package %{nil}
%global __os_install_post \
                    %(echo '%{__os_install_post}' | sed -e '/brp-strip/d')


Name:           spotify-client
Version:        0.9.4.183.g644e24e.428
Release:        4%{?dist}
Summary:        Spotify music player native client

# board=http://community.spotify.com/t5/Desktop-Linux
# $board/What-license-does-the-linux-spotify-client-use/td-p/173356
License:        No modification permitted, non-redistributable
URL:            http://www.spotify.com/se/blog/archives/2010/07/12/linux/
Group:          Applications/Multimedia
ExclusiveArch:  i386 i686 x86_64
Source0:        %{github_repo}/spotify-make-%{version}-%{shortcommit}.tar.gz
Source1:        %{repo}/spotify-client_%{version}-1_amd64.deb
Source2:        %{repo}/spotify-client_%{version}-1_i386.deb

%ifarch x86_64
%global   spotify_pkg   %{SOURCE1}
%global   req_64        ()(64bit)
%else
%global   spotify_pkg   %{SOURCE2}
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  python2-devel
BuildRequires:  redhat-lsb-core

Requires:       zenity
Requires:       hicolor-icon-theme
                # Symlinked, not picked up by autorequire (all 5).
Requires:       libnspr4.so%{?req_64}
Requires:       libplc4.so%{?req_64}
Requires:       libsmime3.so%{?req_64}
Requires:       libnssutil3.so%{?req_64}
Requires:       libnss3.so%{?req_64}

Provides:       spotify = %{version}-%{release}
# https://lists.rpmfusion.org/pipermail/rpmfusion-developers/2012-November/013934.html
Provides:       bundled(libssl) = 0.9.8

%description
Think of Spotify as your new music collection. Your library. Only this time
your collection is vast: millions of tracks and counting.  Spotify comes in
all shapes and sizes, available for your PC, Mac, home audio system and
mobile phone. Wherever you go, your music follows you. And because the music
plays live, there’s no need to wait for downloads and no big dent in your
hard drive.

# Bundled, we should not Provide these. Cannot use %%filter
# due to BZ 873847. Instead, use builtin filtering:
# http://rpm.org/wiki/PackagerDocs/DependencyGenerator
%global __provides_exclude_from  ^%{_libdir}/spotify-client/.*[.]so

# Filter away the deps om bundled libs and those substituted
# by symlinks and explicit Requires:.
%global __requires_exclude                     ^libssl.so.0.9.8
%global __requires_exclude %__requires_exclude|^libcrypto.so.0.9.8
%global __requires_exclude %__requires_exclude|^libcef.so
%global __requires_exclude %__requires_exclude|^libudev.so.0
%global __requires_exclude %__requires_exclude|[.]so[.][0-2][a-f]


%prep
%setup -qn spotify-make-%{commit}


%build
./configure --prefix=/usr --libdir=%{_libdir} --package=%{spotify_pkg}


%install
make install DESTDIR=%{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc opt/spotify/spotify-client/licenses.xhtml
%doc opt/spotify/spotify-client/readme.fedora
%doc opt/spotify/spotify-client/changelog
%{_libdir}/spotify-client
%{_bindir}/spotify
%{_mandir}/man1/spotify.*
%{_datadir}/applications/spotify.desktop
%{_datadir}/icons/hicolor/*/apps/spotify-client.png
%{_datadir}/spotify-client


%changelog
* Sat Oct 12 2013 Alec Leamas <leamas@nowhere.net> - 0.9.4.183.g644e24e.428-4
- Updating to latest spotify-make.
- Still more fixes for directory layout.

* Sat Oct 12 2013 Alec Leamas <leamas@nowhere.net> - 0.9.4.183.g644e24e.428-3
- Updating to latest spotify-make
- Fixes for directory layout in 0.9.4, notably SpotifyHelper in Data.

* Fri Oct 11 2013 Alec Leamas <leamas@nowhere.net> - 0.9.4.183.g644e24e.428-2
- Updating to latest spotify-make
- New spotify release
- Filter new bundled libudev.so.0.

* Mon Jun 17 2013 Alec Leamas <leamas@nowhere.net> - 0.9.1.55.gbdd3b79.203-1
- Updating to latest spotify-make
- New upstream version

* Sun May 05 2013 Alec Leamas <leamas@nowhere.net> - 0.9.0.133.gd18ed58.259-2
- Updating to latest spotify-make.

* Fri May 03 2013 Alec Leamas <leamas@nowhere.net> - 0.9.0.133.gd18ed58.259-1
- Updating to new upstream release

* Fri Jan 04 2013 Alec Leamas <leamas@nowhere.net> - 0.8.8.323.gd143501.250-5
- Rebase to current spotify-make

* Fri Jan 04 2013 Alec Leamas <leamas@nowhere.net> - 0.8.8.323.gd143501.250-4
- Using separate installer providing make install and check-deps, clean up.
- Fixing bad strip if binary

* Fri Jan 04 2013 Alec Leamas <leamas@nowhere.net> - 0.8.8.323.gd143501.250-3
- Install icons properly.
. Reverted rel 2 Icons fix.
- Remove ~/.cache/spotify first time new version runs.

* Fri Jan 04 2013 Alec Leamas <leamas@nowhere.net> - 0.8.8.323.gd143501.250-2
- Added missing Icons link.

* Thu Jan 03 2013 Alec Leamas <leamas@nowhere.net> - 0.8.8.323.gd143501.250-1
- Updating to latest upstream version.

* Thu Dec 20 2012 Alec Leamas <leamas@nowhere.net> - 0.8.4.103.g9cb177b.260-5
- Handle also i386 architecture, F18 uses i386 instead of i686.

* Tue Nov 20 2012 Alec Leamas <leamas@nowhere.net> - 0.8.4.103.g9cb177b.260-4
- Made explicit deps requiring 64-bit libs as required.
- Fixed symlinks (rebase error, old version used).
- Removed explicit GConf2 requirement, not needed.
- Updating license.

* Tue Nov 20 2012 Alec Leamas <leamas@nowhere.net> - 0.8.4.103.g9cb177b.260-3
- Fixed %%install bug (%%buildroot not created before use).
- Wrong path fed to ldd in %%build fixed.

* Tue Nov 13 2012 Alec Leamas <leamas@nowhere.net> - 0.8.4.103.g9cb177b.260-2
- Removing BR: chrpath.
- Cleaning up some shell code.
- Removing explicit libpn12 requirement (works after libcef.se is 755).
- Adding Provides: bundled(...) for libssl.

* Mon Nov 12 2012 Alec Leamas <leamas@nowhere.net> - 0.8.4.103.g9cb177b.260-2
- Handling review remarks...
- Made spotify.sh separate source.
- Updated symlinking of libs: explicit requires + check in %%build, no
  %%ghost, simplified %%files.
- Added manpage.
- Use LD_LIBRARY_PATH instead of rpath.
- Updated wrapper script to handle known bugs.

* Tue Nov 6 2012 Alec Leamas <leamas@nowhere.net> - 0.8.4.103.g9cb177b.260-1
- Initial version


