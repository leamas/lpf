DESTDIR=
PREFIX=/usr
BINDIR=$(PREFIX)/bin
LIBEXECDIR=$(PREFIX)/libexec
DATADIR=$(PREFIX)/share

all:
	echo 'Only "make install" is doing something'.

install:
	install -m 755 -d $(DESTDIR)/etc/sudoers.d
	install -m 755 -d $(DESTDIR)/var/lib/lpf/{packages,rpms,approvals,log}
	install -m 755 -d $(DESTDIR)$(DATADIR)/lpf/packages
	install -m 755 -d $(DESTDIR)$(BINDIR)
	install -m 755 -d $(DESTDIR)$(LIBEXECDIR)

	cp -a pkg-build $(DESTDIR)/etc/sudoers.d
	cp -ar scripts $(DESTDIR)$(DATADIR)/lpf
	ln -s $(DATADIR)/lpf/scripts/lpf $(DESTDIR)$(BINDIR)/lpf
	ln -s $(DATADIR)/lpf/scripts/lpf-kill-pgroup \
	    $(DESTDIR)/$(LIBEXECDIR)/lpf-kill-pgroup

	for size in 24 32 48 64 128; do \
	    install -pm 644 -D icons/lpf-$$size.png \
	        $(DESTDIR)$(DATADIR)/icons/hicolor/$${size}x$${size}/apps/lpf.png; \
	done
	desktop-file-install \
	    --dir $(DESTDIR)$(DATADIR)/applications lpf.desktop
