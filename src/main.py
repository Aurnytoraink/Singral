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
import os
import os.path
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio, Adw, GLib, Gdk

from .window import SingralWindow


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.github.Aurnytoraink.Singral',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        # This is for test
        # In the futur, the app will check on startup if a user as already login or not
        self.logged = False

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
            self.win = SingralWindow(application=self)
        self.win.present()

        # Check if or not the user has already logged in
        if self.logged:
            self.win.main_stack.set_visible_child_name("app_page")
        else:
            self.win.main_stack.set_visible_child_name("login_page")

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
        # Authors of the background picture in the login window
        about.set_artists(
            [
                "Eric Krull"
            ]
        )
        # Translators: Replace "translator-credits" with your names, one name per line
        about.set_translator_credits(_("translator-credits"))
        about.set_website_label(_("GitHub"))
        about.set_website("https://github.com/Aurnytoraink/Singral/")
        about.present()

    def _quit(self,*_):
        self.quit()

def main(version):
    app = Application()
    return app.run(sys.argv)
