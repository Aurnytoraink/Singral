# main.py
#
# Copyright 2020 Aurnytoraink
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio, Adw, GLib, Gdk

#from singral.windows.main_window import MainWindow
from singral.windows.login_window import LoginWindow
from singral.windows.preferences_window import PreferencesWindow


class Application(Gtk.Application):
    def __init__(self, version):
        super().__init__(application_id='com.github.Aurnytoraink.Singral',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.version = version

        GLib.set_application_name("Singral")
        GLib.set_prgname("com.github.Aurnytoraink.Singral")

    def do_startup(self):
        Gtk.Application.do_startup(self)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource('/com/github/Aurnytoraink/Singral/css/style.css')
        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(
            display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self.setup_actions()

        Adw.init()

    def setup_actions(self):
        simple_actions = [
            ('show-preferences', self.show_preferences_window, ('<Ctrl>comma',)),
            ('show-shortcuts', self.show_shortcuts_window, ('<Ctrl>question',)),
            ('show-about', self.show_about_dialog, None),
            ('quit', self.on_quit, ('<Ctrl>q',)),
        ]

        for action, callback, accel in simple_actions:
            simple_action = Gio.SimpleAction.new(action, None)
            simple_action.connect('activate', callback)
            self.add_action(simple_action)
            if accel:
                self.set_accels_for_action(f'app.{action}', accel)

    def do_activate(self):
        self.win = self.props.active_window
        if not self.win:
            self.win = LoginWindow(application=self)
        self.win.present()

    def setup_actions(self):
        simple_actions = [
            ('show-preferences', self.show_preferences_window, ('<Ctrl>comma',)),
            ('show-shortcuts', self.show_shortcuts_window, ('<Ctrl>question',)),
            ('show-about', self.show_about_dialog, None),
            ('quit', self.on_quit, ('<Ctrl>q',)),
        ]

        for action, callback, accel in simple_actions:
            simple_action = Gio.SimpleAction.new(action, None)
            simple_action.connect('activate', callback)
            self.add_action(simple_action)
            if accel:
                self.set_accels_for_action(f'app.{action}', accel)

    def show_preferences_window(self, action, param):
        preferences = PreferencesWindow()
        preferences.set_transient_for(self.props.active_window)
        preferences.show()

    def show_shortcuts_window(self, action, param):
        builder = Gtk.Builder()
        builder.add_from_resource(f'{Constants.PATHID}/ui/shortcuts_window.ui')
        window = builder.get_object('shortcuts')
        window.set_transient_for(self.props.active_window)
        window.present()

    def show_about_dialog(self, action, param):
        about = Gtk.AboutDialog()
        about.set_transient_for(self.props.active_window)
        about.set_modal(True)
        about.set_version(self.version)
        about.set_program_name("Singral")
        about.set_logo_icon_name("com.github.Aurnytoraink.Singral")
        about.set_authors(
            [
                "Mathieu Heurtevin"
            ]
        )
        about.set_comments(_("Qobuz client for GNOME"))
        about.set_wrap_license(True)
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_copyright(_("Copyright 2021 Mathieu Heurtevin"))
        about.set_website_label(_("GitHub"))
        about.set_website("https://github.com/Aurnytoraink/Singral/")
        about.present()

    def on_quit(self,*_):
        self.quit()

def main(version):
    app = Application(version)
    return app.run(sys.argv)
