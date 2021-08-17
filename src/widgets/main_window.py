# main_window.py
#
# Copyright 2021 Aurnytoraink
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

from gi.repository import Gtk, Adw, GObject, GLib, Gdk

@Gtk.Template(resource_path='/com/github/Aurnytoraink/Singral/ui/main_window.ui')
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    main_stack = Gtk.Template.Child()
    app_stack = Gtk.Template.Child()

    music_bin = Gtk.Template.Child()
    podcasts_bin = Gtk.Template.Child()
    favs_bin = Gtk.Template.Child()

    menu_button = Gtk.Template.Child()
    account_info = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.menu_button.get_popover().add_child(self.account_info, "account-info")



