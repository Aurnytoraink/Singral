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
class TidalgtkWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'TidalgtkWindow'

    header_stack = Gtk.Template.Child()
    main_stack = Gtk.Template.Child()
    app_stack = Gtk.Template.Child()
    player_reveal = Gtk.Template.Child()
    switchbar_bottom = Gtk.Template.Child()
    switchbar_bottom = Gtk.Template.Child()
    player_timebar = Gtk.Template.Child()
    play_songinfo = Gtk.Template.Child()
    enlarge_player_button = Gtk.Template.Child()
    reduce_player_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("check-resize",self.update_scale_interface)
        self.enlarge_player_button.connect("clicked",self.resize_player)
        self.reduce_player_button.connect("clicked",self.resize_player)

    def update_scale_interface(self, *_):
        width, height = self.get_size()
        if width <= 545:
            self.header_stack.set_visible_child_name("title_header")
            if self.main_stack.get_visible_child_name() == "app_page":
                self.switchbar_bottom.set_reveal(True)
            self.player_timebar.set_visible(False)
            self.play_songinfo.set_hexpand(True)
        else:
            self.header_stack.set_visible_child_name("switchbar_header")
            self.switchbar_bottom.set_reveal(False)
            self.player_timebar.set_visible(True)
            self.play_songinfo.set_hexpand(False)

    def resize_player(self, *_):
        if self.main_stack.get_visible_child_name() == "app_page":
            self.main_stack.set_visible_child_name("player_page")
            self.switchbar_bottom.set_reveal(False)
            self.player_reveal.set_reveal_child(False)
        elif self.main_stack.get_visible_child_name() == "player_page":
            self.main_stack.set_visible_child_name("app_page")
            self.switchbar_bottom.set_reveal(True)
            self.player_reveal.set_reveal_child(True)

            
