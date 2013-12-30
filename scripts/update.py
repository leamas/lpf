#!/usr/bin/env python

''' Update package GUI. '''

import os.path
import os
import signal
import subprocess
import sys

from gi.repository import GLib        # pylint: disable=no-name-in-module
from gi.repository import Gtk         # pylint: disable=no-name-in-module


def _goodbye():
    ''' Kill everything we've started. '''
    kill_pgroup = os.path.dirname(os.path.abspath(__file__)) + \
        "/lpf-kill-pgroup"
    subprocess.call([kill_pgroup])
    sys.exit(1)


class UpdateHandler(object):
    ''' FSM GUI accepting user commands and input from script to update. '''

    def __init__(self, builder_):
        self.builder = builder_
        self._state = 'init'
        self._icons = [None, None, None, None, None]
        builder_.get_object('ok_btn').set_sensitive(False)
        builder_.get_object('buildlog_btn').set_sensitive(False)

    def _set_icon(self, row, widget):
        ''' Set icon in row to good, bad or spinning. '''
        table = self.builder.get_object('feedback_table')
        if self._icons[row]:
            table.remove(self._icons[row])
        table.attach(widget, 0, 1, row - 1, row, 0, 0, 20, 5)
        widget.show()
        if isinstance(widget, Gtk.Spinner):
            widget.start()
        self._icons[row] = widget

    def _do_init(self, line):
        ''' Setup default GUI. '''
        if 'build dependencies' in line:
            self._set_icon(1, Gtk.Spinner())
            self._state = 'builddeps'
            dialog = self.builder.get_object("main_dlg")
            try:
                title = "lpf: " + line.split(':')[0]
                dialog.set_title(title)
            except ValueError:
                pass
            dialog.show_all()

    def _do_builddeps(self, line):
        ''' Process input line in state builddeps. '''
        if 'downloading' in line:
            self._set_icon(1, Gtk.Image(stock=Gtk.STOCK_YES))
            self._set_icon(2, Gtk.Spinner())
            self._state = 'downloading'
        elif 'rror' in line:
            self._set_icon(3, Gtk.Image(stock=Gtk.STOCK_NO))
            self._state = 'failed'

    def _do_download(self, line):
        ''' Process input line in state downloading. '''
        if 'building' in line:
            self._set_icon(2, Gtk.Image(stock=Gtk.STOCK_YES))
            self._set_icon(3, Gtk.Spinner())
            self._state = 'building'
        elif 'rror' in line:
            self._set_icon(1, Gtk.Image(stock=Gtk.STOCK_NO))
            self._state = 'failed'

    def _do_build(self, line):
        ''' Process input line in state building. '''
        if 'installation error' in line:
            self._set_icon(3, Gtk.Image(stock=Gtk.STOCK_YES))
            self._set_icon(4, Gtk.Image(stock=Gtk.STOCK_NO))
            self._state = 'done'
        elif 'install completed' in line:
            self._set_icon(4, Gtk.Image(stock=Gtk.STOCK_YES))
            self._state = 'done'
        elif 'build completed' in line:
            self._set_icon(3, Gtk.Image(stock=Gtk.STOCK_YES))
        elif 'rror' in line:
            self._set_icon(3, Gtk.Image(stock=Gtk.STOCK_NO))
            self._state = 'failed'
        elif 'installing' in line:
            self._set_icon(3, Gtk.Image(stock=Gtk.STOCK_YES))
            self._set_icon(4, Gtk.Spinner())
            self._state = 'installing'

    def _do_install(self, line):
        ''' Process input line in state installing. '''
        if 'install completed' in line:
            self._set_icon(4, Gtk.Image(stock=Gtk.STOCK_YES))
            self._state = 'done'
        elif 'installation errors' in line or 'no rpms to install' in line:
            self._set_icon(4, Gtk.Image(stock=Gtk.STOCK_NO))
            self._state = 'done'

    # pylint: disable=unused-argument
    def process_line(self, source, cb_condition):
        ''' Parse input line from update script. '''
        l = sys.stdin.readline()
        print l.rstrip()
        if self._state == 'init':
            self._do_init(l)
        elif self._state == 'builddeps':
            self._do_builddeps(l)
        elif self._state == 'downloading':
            self._do_download(l)
        elif self._state == 'building':
            self._do_build(l)
        elif self._state == 'installing':
            self._do_install(l)
        if self._state in ['done', 'failed']:
            self.builder.get_object('ok_btn').set_sensitive(True)
            builder.get_object('buildlog_btn').set_sensitive(True)
        return True


class Handler(object):
    ''' default glade event handlers. '''
    # pylint: disable=missing-docstring, unused-argument

    def on_build_error_dialog_destroy(self, *args):
        print "close"
        Gtk.main_quit(*args)
        sys.exit(1)

    def on_build_error_dialog_close(self, *args):
        print "close"
        Gtk.main_quit(*args)
        sys.exit(1)

    def on_buildlog_btn_clicked(self, button):
        lpf = os.path.dirname(os.path.abspath(__file__)) + "/lpf"
        subprocess.call([lpf, 'log'])

    def on_ok_btn_clicked(self, button):
        Gtk.main_quit(self, button)
        sys.exit(0)

    def on_cancel_btn_clicked(self, button):
        _goodbye()


#pylint: disable=invalid-name
signal.signal(signal.SIGPIPE, signal.SIG_IGN)

builder = Gtk.Builder()
ui = os.path.dirname(os.path.abspath(__file__)) + "/update.ui"
builder.add_from_file(ui)
builder.connect_signals(Handler())

update_handler = UpdateHandler(builder)
GLib.io_add_watch(0, GLib.IO_IN, update_handler.process_line)
Gtk.main()
