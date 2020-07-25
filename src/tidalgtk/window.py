# window.py
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

from gi.repository import Gtk, Handy
# from tidalgtk.api.session import Session

@Gtk.Template(resource_path='/com/github/Aurnytoraink/TidalGTK/ui/window.ui')
class TidalgtkWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'TidalgtkWindow'

    app_stack = Gtk.Template.Child()
    switchbar_bottom = Gtk.Template.Child()
    player_timebar = Gtk.Template.Child()
    play_songinfo = Gtk.Template.Child()
    enlarge_player_button = Gtk.Template.Child()
    close_player_button = Gtk.Template.Child()
    deck_app = Gtk.Template.Child()
    header_switch = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("check-resize",self.update_scale_interface)
        self.enlarge_player_button.connect("clicked",self.display_player)
        self.close_player_button.connect("clicked",self.display_player)

    def update_scale_interface(self, *_):
        if self.header_switch.get_title_visible():
            self.switchbar_bottom.set_reveal(True)
            self.player_timebar.set_visible(False)
            self.play_songinfo.set_hexpand(True)
        else:
            self.switchbar_bottom.set_reveal(False)
            self.player_timebar.set_visible(True)
            self.play_songinfo.set_hexpand(False)

    def display_player(self, *_):
        if self.deck_app.get_visible_child_name() == "app_page":
            self.deck_app.set_visible_child_name("player_page")
            self.switchbar_bottom.set_reveal(False)
            self.player_reveal.set_reveal_child(False)
        elif self.deck_app.get_visible_child_name() == "player_page":
            self.deck_app.set_visible_child_name("app_page")
            self.switchbar_bottom.set_reveal(True)
            self.player_reveal.set_reveal_child(True)

            
