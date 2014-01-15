''' Simple build error dialog, access to logs etc. '''

import os.path
import os
os.environ['NO_AT_BRIDGE'] = '0'

from gi.repository import Gtk        # pylint:disable=no-name-in-module


class Handler(object):
    ''' Implicit signal handlers declared in glade. '''

    def on_build_error_dialog_destroy(self, *args):
        ''' Window closed using window manager. '''
        Gtk.main_quit(*args)

    def on_build_error_dialog_close(self, *args):
        ''' User pushes Close button '''
        Gtk.main_quit(*args)

    def on_view_buildlog_button_clicked(self, button):
        ''' User pushes 'View buildlog' button. '''
        Gtk.main_quit(self, button)

    def on_ok_button_clicked(self, button):
        ''' User pushes 'OK' button. '''
        Gtk.main_quit(self, button)


def main():
    ''' Indeed: main function... '''
    builder = Gtk.Builder()
    ui = os.path.dirname(os.path.abspath(__file__)) + "/build-error.ui"
    builder.add_from_file(ui)
    builder.connect_signals(Handler())
    window = builder.get_object('build_error_dialog')
    window.show_all()

    Gtk.main()


if __name__ == '__main__':
    main()


# vim: set expandtab ts=4 sw=4:
