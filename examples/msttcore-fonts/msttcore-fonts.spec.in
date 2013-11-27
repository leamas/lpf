%global fontname msttcore
%global fontconf 70-%{fontname}.conf

# directory to unpack truetype fonts from the cab into
%global fontdir %{_datadir}/fonts/%{fontname}

%global sf_corefonts http://downloads.sourceforge.net/corefonts/the%20fonts/final

Summary:   Microsoft core TrueType fonts for better Windows Compatibility
Name:      %{fontname}-fonts
Version:   2.2
Release:   1

URL:       http://mscorefonts2.sourceforge.net/
License:   non-redistributable
Group:     User Interface/X
BuildArch: noarch
Obsoletes: msttcorefonts <= 2.0-3
Provides:  msttcorefonts = 2.2-1
Requires:  cabextract
Requires:  xorg-x11-font-utils
Requires:  fontconfig

Source0:   http://sourceforge.net/projects/mscorefonts2/files/cabs/EUupdate.EXE
Source1:   %{sf_corefonts}/andale32.exe
Source2:   %{sf_corefonts}/arialb32.exe
Source3:   %{sf_corefonts}/comic32.exe
Source4:   %{sf_corefonts}/courie32.exe
Source5:   %{sf_corefonts}/georgi32.exe
Source6:   %{sf_corefonts}/impact32.exe
Source7:   %{sf_corefonts}/webdin32.exe
Source8:   %{sf_corefonts}/wd97vwr32.exe
Source20:  msttcore-fonts-fontconfig.conf


%description
TrueType core fonts for the web that were once
available from http://www.microsoft.com/typography/fontpack/ prior
to 2002, and most recently updated in the European Union Expansion
Update circa May 2007, still available on the Microsoft website.

These are the fonts added:

    1998 Andale Mono
    2006 Arial: bold, bold italic, italic, regular
    1998 Arial: black
    1998 Comic: bold, regular
    2000 Courier: bold, bold italic, italic, regular
    1998 Impact
    2006 Times: bold, bold italic, italic, regular
    2006 Trebuchet: bold, bold italic, italic, regular
    2006 Verdana: bold, bold italic, italic, regular
    1998 Webdings


%prep
%setup -cT
for src in  %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} \
    %{SOURCE5} \ %{SOURCE6} %{SOURCE7} %{SOURCE8}
do
    cabextract $src
done



%install
install -d  $RPM_BUILD_ROOT/%{fontdir}
install -m 644 -p *.ttf *.TTF $RPM_BUILD_ROOT/%{fontdir}
install -m 0755 -d $RPM_BUILD_ROOT%{_fontconfig_templatedir} \
                   $RPM_BUILD_ROOT%{_fontconfig_confdir}
install -m 0644 -p %{SOURCE20} \
      $RPM_BUILD_ROOT%{_fontconfig_templatedir}/%{fontconf}
ln -s %{_fontconfig_templatedir}/%{fontconf} \
      $RPM_BUILD_ROOT%{_fontconfig_confdir}/%{fontconf}

mkdir -p $RPM_BUILD_ROOT/etc/X11/xorg.conf.d/
cat -> $RPM_BUILD_ROOT/etc/X11/xorg.conf.d/09-msttcore-fontpath.conf <<'EOT'
Section "Files"
  FontPath "%{fontdir}"
EndSection
EOT


%_font_pkg -f %{fontconf} *.ttf *.TTF
%config(noreplace) /etc/X11/xorg.conf.d/09-msttcore-fontpath.conf
%doc License.txt Licen.TXT


%changelog
* Tue May 28 2013 Alec Leamas <leamas@nowhere.net> 2.1-3
- Adapting to lpf, don't download in scriptlets.
- Base on font package template
- Rename to offical -fonts suffix

* Mon Sep 15 2012  Rob Janes <janes.rob gmail com> 2.1-2
- updated comments, messages, description and such.
- don't download older cabs for fonts in the EUupdate.EXE file,
  unless the download for the EUupdate failed.
- available at
https://downloads.sourceforge.net/project/mscorefonts2/specs/msttcore-fonts-2.1-2.spec

* Sat Sep 8 2012  Rob Janes <janes.rob gmail com> 2.1-1
- generates distributable rpm that downloads and unpacks the fonts at
  install time, not rpmbuild time
- available at
https://downloads.sourceforge.net/project/mscorefonts2/specs/msttcore-fonts-2.1-1.spec

* Sat Sep 8 2012  Rob Janes <janes.rob gmail com> 2.0-7
- added EUupdate.EXE European Union Expansion Update circa May 2007
- refactored sourceforge mirror stuff
- replaced wget with curl, which seems to be installed by default on fedora
- replaced ttmkfdir with mkfontscale and mkfontdir.  This creates fonts.dir file
  for the core X font system.  ttmkfdir has been supersceded by mkfontdir - they
  both create fonts.dir but mkfontdir is part of xorg-x11-font-utils.
- removed 09-msttcorefonts.conf and refactored fc-cache lines.  fc-cache walks
  subdirectories so the 09-msttcorefonts.conf to add the /usr/share/font/msttcore
  is redundant.  fc-cache indexes for the Xft font system, not the legacy core X
  font system.
- added 09-msttcore-fontpath.conf to /etc/X11/xorg.conf.d for core X font system
- added xset fp+ to add the fontdirectory to core X font for the current session so
  the installer doesn't have to relogin.
- available at
https://downloads.sourceforge.net/project/mscorefonts2/specs/msttcore-fonts-2.0-7.spec

* Mon Aug 15 2011  Dennis Johnson
- BuildRequires ttmkfdir, cabextract, wget
- removes Requires
- fixes sourceforge mirror
- generates 09-msttcorefonts.conf
- restores call to ttmkfdir in install section
- available from http://fenris02.fedorapeople.org/msttcore-fonts-2.0-6.spec

* Sat Dec 11 2010  Hnr Kordewiner <hnr@kordewiner.com> 2.0-5
- move 09-msttcorefonts.conf to this spec file
- drop %{ttmkfdir} - again
- msttcore fonts history site setup at http://moin.kordewiner.com/helpdesk/fedora/mscorefonts
- available from http://moin.kordewiner.com/helpdesk/fedora/mscorefonts?action=AttachFile&do=get&target=msttcore-fonts-2.0-5.spec

* Mon Jun 07 2010 Zied FAKHFAKH <fzied@dottn.com> 2.0-3
- removed chkfontpath dependency for Fedora >= 9
- removed prerun and post chkconfig reference
- divergent development, same purpose as Andrew Bartlett's but derived from Noa Resare's 2.0-1
- available from http://moin.kordewiner.com/helpdesk/fedora/mscorefonts?action=AttachFile&do=get&target=msttcorefonts-2.0-3.spec

* Tue Jun 16 2009  Dennis Johnson
- Provides msttcorefonts
- Requires ttmkfdir, cabextract
- restores call to ttmkfdir in install section
- available from http://fenris02.fedorapeople.org/msttcore-fonts-2.0-4.spec

* Wed Jun 25 2008  Muayyad Saleh Alsadi <alsadi gmail com> 2.0-3
- drop %{ttmkfdir} completely

* Mon Feb 18 2008 Andrew Bartlett <abartlet samba org> 2.0-2
- Make work with Fedora 9 fonts system
- available from http://moin.kordewiner.com/helpdesk/fedora/mscorefonts?action=AttachFile&do=get&target=msttcorefonts-2.0-2.spec

* Sun May 07 2006 Noa Resare <noa resare com> 2.0-1
- checksums downloads
- random mirror
- use redistributable word 97 viewer as source for tahoma.ttf
- available from http://corefonts.sourceforge.net/msttcorefonts-2.0-1.spec

* Mon Mar 31 2003 Daniel Resare <noa resare com> 1.3-4
- updated microsoft link
- updated sourceforge mirrors

* Mon Nov 25 2002 Daniel Resare <noa resare com> 1.3-3
- the install dir is now deleted when the package is uninstalled
- executable permission removed from the fonts
- executes fc-cache after install if it is available

* Thu Nov 07 2002 Daniel Resare <noa resare com> 1.3-2
- Microsoft released a new service-pack. New url for Tahoma font.

* Thu Oct 24 2002 Daniel Resare <noa resare com> 1.3-1
- removed python hack
- removed python hack info from description
- made tahoma inclusion depend on define
- added some info on the ttmkfdir define

* Tue Aug 27 2002 Daniel Resare <noa resare com> 1.2-3
- fixed spec error when tahoma is not included

* Tue Aug 27 2002 Daniel Resare <noa resare com> 1.2-2
- removed tahoma due to unclear licensing
- parametrized ttmkfdir path (for mandrake users)
- changed description text to reflect the new microsoft policy

* Thu Aug 15 2002 Daniel Resare <noa resare com> 1.2-1
- changed distserver because microsoft no longer provides them

* Tue Apr 09 2002 Daniel Resare <noa resare com> 1.1-3
- fixed post/preun script to actually do what they were supposed to do

* Tue Mar 12 2002 Daniel Resare <noa resare com> 1.1-2
- removed cabextact from this package
- added tahoma font from ie5.5 update

* Fri Aug 25 2001 Daniel Resare <noa metamatrix se>
- initial version

