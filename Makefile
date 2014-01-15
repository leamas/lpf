DESTDIR=
PREFIX=/usr
BINDIR=$(PREFIX)/bin
LIBEXECDIR=$(PREFIX)/libexec
DATADIR=$(PREFIX)/share
RPM_MACROS_DIR=/usr/lib/rpm/macros.d
MAN1=$(DATADIR)/man/man1

HICOLORDIR=$(DESTDIR)$(DATADIR)/icons/hicolor

all:
	echo 'Only "make install" is doing something'.

install:
	install -m 755 -d $(DESTDIR)/var/lib/lpf/{packages,rpms,approvals,log}
	install -m 755 -d $(DESTDIR)/var/lib/lpf/notify
	install -m 755 -d $(DESTDIR)$(DATADIR)/lpf/packages
	install -m 755 -d $(DESTDIR)$(DATADIR)/lpf/icons
	install -m 755 -d $(DESTDIR)$(BINDIR)
	install -m 755 -d $(DESTDIR)$(LIBEXECDIR)
	install -m 755 -d $(DESTDIR)$(MAN1)

	install -pDm 640 pkg-build.sudo $(DESTDIR)/etc/sudoers.d/pkg-build
	install -pDm 644 macros.lpf $(DESTDIR)$(RPM_MACROS_DIR)/macros.lpf
	install -pDm 644 appdata/lpf.appdata.xml \
	     $(DESTDIR)$(DATADIR)/appdata/lpf.appdata.xml
	cp -ar scripts CONFIG $(DESTDIR)$(DATADIR)/lpf
	cp -a lpf-notify.desktop $(DESTDIR)$(DATADIR)/lpf
	cp -a lpf.1 lpf-gui.1 $(DESTDIR)$(DATADIR)/lpf
	cp -a icons/*.png $(DESTDIR)$(DATADIR)/lpf/icons
	rm -f  $(DESTDIR)$(DATADIR)/lpf/scripts/pylint.conf
	cp -ar scripts CONFIG version $(DESTDIR)$(DATADIR)/lpf
	ln -s $(DATADIR)/lpf/scripts/lpf $(DESTDIR)$(BINDIR)/lpf
	ln -s $(DATADIR)/lpf/scripts/lpf-gui $(DESTDIR)$(BINDIR)/lpf-gui
	ln -s $(DATADIR)/lpf/scripts/lpf-kill-pgroup \
	    $(DESTDIR)/$(LIBEXECDIR)/lpf-kill-pgroup

	for size in 24 32 48 64 128; do \
	    install -pm 644 -D icons/lpf-$$size.png \
	        $(HICOLORDIR)/$${size}x$${size}/apps/lpf.png; \
	done
	for size in 24 32 48 ; do \
	    install -pm 644 -D icons/lpf-gui-$$size.png \
	        $(HICOLORDIR)/$${size}x$${size}/apps/lpf-gui.png; \
	done
	cp -a lpf.1 lpf-gui.1  $(DESTDIR)$(MAN1)
	desktop-file-install \
	    --dir $(DESTDIR)$(DATADIR)/applications lpf.desktop
	desktop-file-install \
	    --dir $(DESTDIR)$(DATADIR)/applications lpf-gui.desktop
	desktop-file-install \
	    --dir $(DESTDIR)$(DATADIR)/applications lpf-notify.desktop

pylint:
	@PYTHONPATH=scripts pylint --rcfile=pylint.conf \
	    scripts/lpf-gui \
	    scripts/lpf_gui_base.py \
	    scripts/update.py
