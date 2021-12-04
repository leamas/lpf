''' Simple notification dialog. '''

import os
import os.path
import subprocess
os.environ['NO_AT_BRIDGE'] = '0'

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk         # pylint: disable=no-name-in-module
from gi.repository import GObject     # pylint: disable=no-name-in-module


def here(path):
    ' Return path added to current dir for __FILE__. '
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)


def get_outdated():
    ''' Return list of packages not in 'OK' state. '''
    statebytes = subprocess.check_output([here('lpf'), 'state'])
    statelines = statebytes.decode('utf-8').split('\n')
    outdated = []
    for stateline in statelines:
        try:
            pkg_name, state = stateline.split()[0:2]
        except (ValueError, IndexError):
            continue
        if state != 'OK':
            outdated.extend([pkg_name])
    return outdated


class Handler(object):
    ''' Init window and handle signals. '''

    def __init__(self, builder_):
        outdated = get_outdated()
        self.builder = builder_
        self.outdated = outdated
        text = "Some lpf packages needs to be updated: "
        text += ','.join(outdated)
        builder_.get_object('message_label').set_text(text)

    @staticmethod
    def on_delete_event_cb(window_, event):
        ''' User just closed window. '''
        Gtk.main_quit()

    def on_checkbox_toggled_cb(self, widget, data=None):
        ''' User checked the "Don't show this message" again checkbox. '''
        if not widget.get_active():
            return
        for pkg_name in self.outdated:
            try:
                subprocess.check_call([here('lpf'), 'mute', pkg_name])
            except subprocess.CalledProcessError:
                pass

    def on_lpf_button_clicked_cb(self, widget, data=None):
        ''' User clicked 'Run lpf' button. '''

        def do_lpf_update():
            ''' Do the dirty wwork. '''
            try:
                subprocess.call([here('lpf'), 'update'])
            except subprocess.CalledProcessError:
                pass
            Gtk.main_quit()

        self.builder.get_object('main_window').hide()
        GObject.idle_add(do_lpf_update)

    @staticmethod
    def on_quit_button_clicked_cb(widget, data=None):
        ''' User clicked 'Quit' button. '''
        Gtk.main_quit()

def main():
    ''' Indeed: main program. '''
    subprocess.check_call([here('lpf-notify'), 'lock'])
    builder = Gtk.Builder()
    builder.add_from_file(here("notify.ui"))
    builder.connect_signals(Handler(builder))
    builder.get_object('main_window').show_all()

    Gtk.main()

    subprocess.check_call([here('lpf-notify'), 'unlock'])


if __name__ == '__main__':
    main()


# vim: set expandtab ts=4 sw=4:
