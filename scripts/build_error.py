#!/usr/bin/env python
''' Simple build error dialog, access to logs etc. '''

import os.path
import os
os.environ['NO_AT_BRIDGE'] = '0'

from gi.repository import Gtk


class Handler(object):

    def on_build_error_dialog_destroy(self, *args):
        print "close"
        Gtk.main_quit(*args)

    def on_build_error_dialog_close(self, *args):
        print "close"
        Gtk.main_quit(*args)

    def on_view_buildlog_button_clicked(self, button):
        print "view_buildlog"
        Gtk.main_quit(self, button)

    def on_ok_button_clicked(self, button):
        print "ok"
        Gtk.main_quit(self, button)


builder = Gtk.Builder()
ui = os.path.dirname(os.path.abspath(__file__)) + "/build-error.glade"
builder.add_from_file(ui)
builder.connect_signals(Handler())
window = builder.get_object('build_error_dialog')
window.show_all()

Gtk.main()
