''' Update package GUI. '''

import os.path
import os
import signal
import subprocess
import sys

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import GLib        # pylint: disable=no-name-in-module
from gi.repository import Gtk         # pylint: disable=no-name-in-module


def _goodbye():
    ''' Kill everything we've started. '''
    kill_pgroup = os.path.dirname(os.path.abspath(__file__)) + \
        "/lpf-kill-pgroup"
    subprocess.call([kill_pgroup])
    sys.exit(1)

# header_label
class UpdateHandler(object):
    ''' FSM GUI accepting user commands and input from script to update. '''

    def __init__(self, builder_):
        self.builder = builder_
        self._state = 'init'
        self._icons = [None, None, None, None, None]
        self._package = None
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
                self._package = line.split(':')[0]
                dialog.set_title("lpf: " + self._package)
                self.builder.get_object("header_label").set_text(
                    "Updating: " + self._package)
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
            self.builder.get_object("header_label").set_text(
                "Updating: " + self._package + ', completed OK.')
        elif 'installation errors' in line or 'no rpms to install' in line:
            self._set_icon(4, Gtk.Image(stock=Gtk.STOCK_NO))
            self._state = 'done'
            self.builder.get_object("header_label").set_text(
                "Updating: " + self._package + ', failed.')

    # pylint: disable=unused-argument
    def process_line(self, source, cb_condition):
        ''' Parse input line from update script. '''
        l = sys.stdin.readline()
        print(l.rstrip())
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
            self.builder.get_object('buildlog_btn').set_sensitive(True)
        return True


class Handler(object):
    ''' Default glade event handlers. '''
    # pylint: disable=unused-argument

    def on_main_dialog_delete(self, *args):
        ''' user closed window using window manager. '''
        Gtk.main_quit(*args)
        sys.exit(1)

    def on_build_error_dialog_close(self, *args):
        ''' User pushed Close button. '''
        Gtk.main_quit(*args)
        sys.exit(1)

    def on_buildlog_btn_clicked(self, button):
        ''' User pushed 'View buildlog' button.'''
        lpf = os.path.dirname(os.path.abspath(__file__)) + "/lpf"
        subprocess.call([lpf, 'log'])

    def on_ok_btn_clicked(self, button):
        ''' User pushed OK button. '''
        Gtk.main_quit(self, button)
        sys.exit(0)

    def on_cancel_btn_clicked(self, button):
        ''' User pushed Cancel button. '''
        _goodbye()


def main():
    ''' Indeed: main program. '''
    builder = Gtk.Builder()
    ui = os.path.dirname(os.path.abspath(__file__)) + "/update.ui"
    builder.add_from_file(ui)
    builder.connect_signals(Handler())

    update_handler = UpdateHandler(builder)
    GLib.io_add_watch(0, GLib.IO_IN, update_handler.process_line)
    Gtk.main()


if __name__ == '__main__':
    signal.signal(signal.SIGPIPE, signal.SIG_IGN)
    main()



# vim: set expandtab ts=4 sw=4:
