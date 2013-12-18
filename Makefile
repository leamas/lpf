DESTDIR=
PREFIX=/usr
BINDIR=$(PREFIX)/bin
LIBEXECDIR=$(PREFIX)/libexec
DATADIR=$(PREFIX)/share
RPM_MACROS_DIR=/usr/lib/rpm/macros.d
MAN1=$(DATADIR)/man/man1

all:
	echo 'Only "make install" is doing something'.

install:
	install -m 755 -d $(DESTDIR)/var/lib/lpf/{packages,rpms,approvals,log}
	install -m 755 -d $(DESTDIR)/var/lib/lpf/notify
	install -m 755 -d $(DESTDIR)$(DATADIR)/lpf/packages
	install -m 755 -d $(DESTDIR)$(BINDIR)
	install -m 755 -d $(DESTDIR)$(LIBEXECDIR)
	install -m 755 -d $(DESTDIR)$(MAN1)

	install -pDm 640 pkg-build.sudo $(DESTDIR)/etc/sudoers.d/pkg-build
	install -pDm 644 macros.lpf $(DESTDIR)$(RPM_MACROS_DIR)/macros.lpf
	cp -ar scripts CONFIG $(DESTDIR)$(DATADIR)/lpf
	ln -s $(DATADIR)/lpf/scripts/lpf $(DESTDIR)$(BINDIR)/lpf
	ln -s $(DATADIR)/lpf/scripts/lpf-kill-pgroup \
	    $(DESTDIR)/$(LIBEXECDIR)/lpf-kill-pgroup

	for size in 24 32 48 64 128; do \
	    install -pm 644 -D icons/lpf-$$size.png \
	        $(DESTDIR)$(DATADIR)/icons/hicolor/$${size}x$${size}/apps/lpf.png; \
	done
	cp -a lpf.1  $(DESTDIR)$(MAN1)
	desktop-file-install \
	    --dir $(DESTDIR)$(DATADIR)/applications lpf.desktop
