''' Main UI: list and update packages. '''


import os
import os.path
import shutil
import subprocess
import sys
import time

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk              # pylint:disable=no-name-in-module
from gi.repository import Gdk              # pylint:disable=no-name-in-module
from gi.repository import GObject          # pylint:disable=no-name-in-module
from gi.repository.Pango import FontDescription  # pylint: disable=F0401,E0611

import version

VERSION = "Version: %s ( %s %s )" % (
    version.VERSION, version.COMMIT, version.DATE.split()[0] )

_HERE = os.path.dirname(os.path.realpath(__file__))
_USER_NOTIFIER_TEMPLATE = os.path.join(_HERE, '..', 'lpf-notify.desktop')


def set_hourglass_cursor(builder):
    ' Use the hourglass cursor to mark long operations. '
    cursor = Gdk.Cursor.new(Gdk.CursorType.WATCH)
    builder.get_object('main_window').get_root_window().set_cursor(cursor)


def set_arrow_cursor(builder):
    ' Use the default arrow cursor.'
    cursor = Gdk.Cursor.new(Gdk.CursorType.ARROW)
    builder.get_object('main_window').get_root_window().set_cursor(cursor)


def here(path):
    ' Return path added to current dir for __FILE__. '
    return os.path.join(_HERE, path)


def icon_path(icon):
    ' Return icon path added to icon. '
    return os.path.join(_HERE, '..', 'icons', icon)


def do_build_cmd(handler, cmd):
    ''' Run a build command. '''

    def do_build():
        ''' Do the dirty work. '''
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError:
            pass
        if handler.window_name == 'overview':
            handler.update_main_grid()
        else:
            handler.update_details(handler.window_name)
        handler.builder.get_object('main_window').set_sensitive(True)

    handler.builder.get_object('main_window').set_sensitive(False)
    GObject.idle_add(do_build)


class Handler(GObject.GObject):
    ''' Handle the GUI signals. '''

    def _find_in_menu(self, menu, condition):
        '''Find item in menu for which condition(item) is true. '''
        for item in self.builder.get_object(menu).get_children():
            try:
                if condition(item):
                    return(item)
            except AttributeError:
                continue
        return None

    @staticmethod
    def pkg_label(pkg_name):
        ''' Label for package in main window. '''
        label = Gtk.Label(pkg_name)
        label.set_text(pkg_name)
        label.set_alignment(0, 0.5)
        return label

    @staticmethod
    def pkg_icon(state):
        ''' Icon for package in main window. '''
        image = Gtk.Image()
        if state == 'OK':
            icon = 'ok.png'
        elif state in ['approve-wait', 'build-wait']:
            icon = 'unbuilt.png'
        else:
            icon = 'error.png'
        image.set_from_file(icon_path(icon))
        image.set_padding(10, 10)
        return image

    def show_log(self):
        ''' Read-only log display in a textview. '''

        def cb_on_view_ok_btn_clicked(button, data=None):
            ''' OK button on view_some_text window. '''
            button.get_toplevel().hide()
            return True

        def cb_on_window_delete_event(window, event):
            ''' Generic window close event. '''
            window.hide()
            return True

        logfile = '/var/lib/lpf/log/%s.log' % self.window_name
        try:
            with open(logfile) as f:
                log = f.read()
        except OSError:
            print((" Cannot open logfile: " + logfile))
            return None
        textview = self.builder.get_object("view_textview")
        textview.modify_font(FontDescription("Monospace"))
        buf = textview.get_buffer()
        buf.set_text(log)
        w = self.builder.get_object('view_window')
        w.set_title("LPF: logfile")
        w.connect('delete-event', cb_on_window_delete_event)
        b = self.builder.get_object('view_ok_btn')
        b.connect('clicked', cb_on_view_ok_btn_clicked)
        w.set_size_request(600, 600)
        w.show_all()
        return w

    def notify_menuitem_setup(self, pkg_name=None):
        ''' Return menuitem in Notifications menu. '''

        user_notifier = os.path.expanduser(
            '~/.config/autostart/lpf-notify.desktop')

        def on_notify_activate_cb(widget, pkg_name):
            ''' Handle changes in 'Enable notifications' menu item. '''
            if widget.get_active():
                if not os.path.exists(os.path.dirname(user_notifier)):
                    os.mkdir(os.path.dirname(user_notifier))
                if not os.path.exists(user_notifier):
                    shutil.copyfile(_USER_NOTIFIER_TEMPLATE, user_notifier)
                    try:
                        subprocess.call(['gtk-launch', 'lpf-notify'])
                    except subprocess.CalledProcessError:
                        pass
            elif os.path.exists(user_notifier):
                os.unlink(user_notifier)
                try:
                    subprocess.call(['pkill', '-9', '-f', 'notify-watch'])
                except subprocess.CalledProcessError:
                    pass

        def on_pkg_activate_cb(widget, pkg_name):
            ''' Disable notifications for a package menu entry callback. '''
            cmd = 'hide' if widget.get_active() else 'unhide'
            subprocess.check_output([here('lpf-notify'), cmd, pkg_name])
            if pkg_name == self.window_name:
                checkbox = \
                    self.builder.get_object('details_block_notify_checkbox')
                checkbox.set_active(widget.get_active())

        if pkg_name:
            item = Gtk.CheckMenuItem.new_with_label("Mute " + pkg_name)
            try:
                subprocess.check_output([here('lpf-notify'),
                                        'is-hidden',
                                        pkg_name])
                item.set_active(True)
            except subprocess.CalledProcessError:
                item.set_active(False)
            item.connect("activate", on_pkg_activate_cb, pkg_name)
        else:
            item = self.builder.get_object('enable_notify_menuitem')
            item.set_active(os.path.exists(user_notifier))
            item.connect("activate", on_notify_activate_cb, pkg_name)
        return item

    def pkg_view_menuitem(self, pkg_name):
        ''' Return menuitem in View menu for package. '''

        def on_view_item_activate_cb(widget, data=None):
            ''' User clicks on item in view menu. '''
            item = self._find_in_menu('view_menu', lambda i: i.get_active())
            if not item:
                print("Cannot find active view item?!")
                return
            pkg_name = str(item.get_label())
            self.window_name = pkg_name
            self.builder.get_object('main_window').set_title(
                "LPF: " + pkg_name)
            top_widget = self.builder.get_object('main_vbox_align')
            child = top_widget.get_child()
            if child:
                top_widget.remove(child)
            if pkg_name == 'overview':
                new_widget = self.main_window
                self.update_main_grid()
            else:
                new_widget = self.details_window
                self.update_details(pkg_name)
            top_widget.add(new_widget)
            new_widget.show_all()

        radio_group = self.builder.get_object('view_menu').get_children()
        radio_group = \
            [r for r in radio_group if hasattr(r, 'set_active')]
        view_item = Gtk.RadioMenuItem.new_with_label(radio_group, pkg_name)
        view_item.connect("activate", on_view_item_activate_cb, self)
        return view_item

    def pkg_build_button(self, pkg_name):
        ''' Return Build... button for package in main window. '''

        def on_build_clicked_cb(button, pkg_name):
            ''' Build button for one package clicked callback. '''
            do_build_cmd(self, [here('lpf'), 'update', pkg_name])

        button = Gtk.Button()
        button.set_label('Build...')
        button.set_border_width(10)
        button.connect("clicked", on_build_clicked_cb, pkg_name)
        return button

    def pkg_more_button(self, pkg_name):
        ''' Return More... button for package in main window. '''

        def on_details_more_button_cb(widget, data=None):
            ''' User clicked on build button in details window. '''
            item = self._find_in_menu('view_menu',
                                      lambda i: i.get_label() == pkg_name)
            if not item:
                print("Cannot find active view item?!")
                return
            item.set_active(True)

        button = Gtk.Button()
        button.set_label('More...')
        button.set_border_width(10)
        button.connect("clicked", on_details_more_button_cb, pkg_name)
        return button

    def get_grid(self):
        ''' Grid replacing original table in main window. '''
        grid = Gtk.Grid()
        grid.set_border_width(10)
        table_align = self.builder.get_object("main_table_align")
        for child in table_align.get_children():
            table_align.remove(child)
        table_align.add(grid)
        return grid

    def get_about(self):
        ''' Install the Help | About dialog. '''
        # See: https://developer.gnome.org/gtk3/stable/GtkAboutDialog.html
        about = Gtk.AboutDialog()
        about.set_program_name('LPF - Local Package Factory')
        about.set_version(VERSION)
        about.set_logo_icon_name('lpf')
        about.set_copyright("Copyright \xc2\xa9 2013-2014 Alec Leamas")
        #about.set_authors(authors)
        about.set_website("http://github.com/leamas/lpf")
        about.set_website_label("Github project home")
        about.connect("response", lambda w, d: w.hide())
        self.builder.get_object("about_item").connect("activate",
                                                      lambda w, a: a.show(),
                                                      about)

    def update_main_grid(self, statelines=None):
        ''' Update the main window grid with data from 'lpf state'. '''
        if not statelines:
            statebytes = subprocess.check_output([here('lpf'), 'state'])
            statelines = statebytes.decode('utf-8').split('\n')
        grid = self.get_grid()
        for row, stateline in enumerate(statelines):
            try:
                pkg_name, state = stateline.split()[0:2]
            except (ValueError, IndexError):
                continue
            build_button = self.pkg_build_button(pkg_name)
            build_button.set_sensitive(state != 'OK')
            grid.attach(self.pkg_label(pkg_name), 0, row, 1, 1)
            grid.attach(self.pkg_icon(state), 1, row, 1, 1)
            grid.attach(build_button, 2, row, 1, 1)
            grid.attach(self.pkg_more_button(pkg_name), 3, row, 1, 1)
        grid.show_all()
        return grid

    def update_details(self, pkg_name):
        ''' Update data in the details window. '''

        def on_build_clicked_cb(button, pkg_name):
            ''' Build button for one package clicked callback. '''
            do_build_cmd(self, [here('lpf'), 'update', pkg_name])

        def on_reset_clicked_cb(button, pkg_name):
            ''' Reset button for one package clicked callback. '''
            subprocess.call([here('lpf'), 'reset', pkg_name])
            self.update_details(pkg_name)

        statebytes = subprocess.check_output([here('lpf'), 'state', pkg_name])
        stateline = statebytes.decode('utf-8')
        try:
            pkg_name, state, vers = stateline.split()
        except ValueError:
            print(("Cannot update details bad state: " + stateline))
            return
        self.builder.get_object('details_version_value_lbl').set_text(vers)
        try:
            cmd = ['rpm', '-q', '--qf', '%{version}-%{release}', pkg_name]
            target_vers = subprocess.check_output(cmd).decode('utf-8')
        except subprocess.CalledProcessError:
            target_vers = 'Not installed'

        self.builder.get_object(
            'details_build_button').set_sensitive(vers != target_vers)
        self.builder.get_object(
            'details_target_version_value_lbl').set_text(target_vers)
        self.builder.get_object('details_state_value_lbl').set_text(state)
        logfile = '/var/lib/lpf/log/%s.log' % pkg_name
        try:
            logstat = os.stat(logfile)
            logdate = time.ctime(logstat.st_mtime)
        except OSError:
            logdate = '-'
        self.builder.get_object(
            'details_log_date_value_lbl').set_text(logdate)
        self.builder.get_object(
            'details_log_button').set_sensitive(logdate != '-')
        self.builder.get_object("details_build_button").connect(
            "clicked", on_build_clicked_cb, pkg_name)
        self.builder.get_object('reset_button').connect(
            "clicked", on_reset_clicked_cb, pkg_name)
        hidden_box = self.builder.get_object('details_block_notify_checkbox')
        try:
            subprocess.check_call([here('lpf-notify'), 'is-hidden', pkg_name])
            hidden_box.set_active(True)
        except subprocess.CalledProcessError:
            hidden_box.set_active(False)

    def connect(self):
        ''' Connect most static signals. '''

        def on_build_all_clicked_cb(button, data=None):
            ''' Build button in main UI callback. '''
            do_build_cmd(self, [here('lpf'), 'update'])

        def on_manpage_clicked_cb(button, data=None):
            ''' Display manpage... '''

            def do_manpage():
                ''' Do the dirty work. '''
                try:
                    subprocess.call(['yelp', 'man:' + here('../lpf-gui.1')])
                except subprocess.CalledProcessError:
                    pass
                self.builder.get_object('main_window').set_sensitive(True)

            self.builder.get_object('main_window').set_sensitive(False)
            GObject.idle_add(do_manpage)

        def on_main_cancel_clicked_cb(button, data=None):
            ''' Cancel button in main UI callback. '''
            Gtk.main_quit()

        def on_details_notify_checkbox_cb(widget, data=None):
            ''' User changes notifications checkbox in details window.  '''
            find_condition = lambda i: self.window_name in i.get_label()
            item = self._find_in_menu('notifications_menu', find_condition)
            if not item:
                print(("Cannot find view menu item for window: "
                      + self.window_name))
                return
            item.set_active(widget.get_active())

        def on_details_log_button_cb(widget, data=None):
            ''' Show last logfile in read-only window. '''
            self.show_log()

        def on_details_dismiss_btn_cb(widget, data=None):
            ''' User clicks 'Dismiss' button in details window. '''
            self.builder.get_object('overview_item').set_active(True)

        connections = [
            ["menuitem_quit", "activate", Gtk.main_quit],
            ["menuitem_build_all", "activate", on_build_all_clicked_cb],
            ["manpage_item", "activate", on_manpage_clicked_cb],
            ["main_cancel_btn", "clicked", on_main_cancel_clicked_cb],
            ["build_all_btn", "clicked", on_build_all_clicked_cb],
            ["details_block_notify_checkbox",
                "toggled", on_details_notify_checkbox_cb],
            ["details_log_button", "clicked", on_details_log_button_cb],
            ["details_dismiss_btn", "clicked", on_details_dismiss_btn_cb],
            ['main_window', "delete-event", Gtk.main_quit]
        ]

        for [object_id, signal, func] in connections:
            self.builder.get_object(object_id).connect(signal, func)

    def __init__(self, builder):

        def windows_setup():
            ''' Detach the two windows (overview/main) from builder model
            and store as self.main_window and self.details_window.
            '''
            # pylint: disable=attribute-defined-outside-init
            self.details_window = self.builder.get_object('details_vbox')
            self.main_window = self.builder.get_object('main_view_vbox')
            self.builder.get_object('main_vbox').remove(
                self.builder.get_object('details_vbox_align'))
            self.builder.get_object('details_vbox_align').remove(
                self.builder.get_object('details_vbox'))

        GObject.GObject.__init__(self)
        self.builder = builder
        self.window_name = 'overview'
        self.connect()
        self.get_about()
        windows_setup()
        statebytes = subprocess.check_output([here('lpf'), 'state'])
        statelines = statebytes.decode('utf-8').split('\n')
        self.update_main_grid(statelines)
        self.notify_menuitem_setup(None)
        for stateline in statelines:
            try:
                pkg_name = stateline.split()[0]
            except (ValueError, IndexError):
                continue
            notify_item = self.notify_menuitem_setup(pkg_name)
            builder.get_object('notifications_menu').add(notify_item)
            view_item = self.pkg_view_menuitem(pkg_name)
            builder.get_object('view_menu').add(view_item)
        set_arrow_cursor(builder)
        builder.get_object('main_window').show_all()


def main():
    ''' Indeed: main program. '''
    if len(sys.argv) > 2:
        print("Usage: lpf-gui [package]")
        sys.exit(2)
    elif len(sys.argv) == 2:
        try:
            subprocess.call([here('lpf'), 'update', sys.argv[1]])
        except subprocess.CalledProcessError:
            pass
    builder = Gtk.Builder()
    builder.add_from_file(here("lpf-gui.ui"))
    Handler(builder)
    Gtk.main()


if __name__ == '__main__':
    main()



# vim: set expandtab ts=4 sw=4:
