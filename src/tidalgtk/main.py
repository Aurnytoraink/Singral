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

gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Gio, Handy

from .window import TidalgtkWindow


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.github.Aurnytoraink.TidalGTK',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        # This is for test
        # In the futur, the app will check on startup if a user as already login or not
        self.logged = False

    def do_startup(self):
        if os.path.isdir('/var/cache/files') is False:
            os.mkdir('/var/cache/files')
            os.mkdir('/var/cache/files/covers')
            os.mkdir('/var/cache/files/songs')

        Gtk.Application.do_startup(self)
        Handy.init()

    def do_activate(self):
        self.win = self.props.active_window
        if not self.win:
            self.win = TidalgtkWindow(application=self)
        self.win.present()

        # Check if or not the user has already logged in
        if self.logged:
            self.win.main_stack.set_visible_child_name("app_page")
        else:
            self.win.main_stack.set_visible_child_name("login_page")

        # Actions that are used in the favs page
        action = Gio.SimpleAction.new("fav_albums", None)
        action.connect("activate", self.win.get_fav_albums)
        self.add_action(action)

        action = Gio.SimpleAction.new("fav_artists", None)
        action.connect("activate", self.win.get_fav_artists)
        self.add_action(action)

        action = Gio.SimpleAction.new("fav_tracks", None)
        action.connect("activate", self.win.get_fav_tracks)
        self.add_action(action)

        action = Gio.SimpleAction.new("fav_playlists", None)
        action.connect("activate", self.win.get_fav_playlists)
        self.add_action(action)


def main(version):
    app = Application()
    return app.run(sys.argv)
