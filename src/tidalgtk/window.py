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
from tidalgtk.player import Player

@Gtk.Template(resource_path='/com/github/Aurnytoraink/TidalGTK/ui/window.ui')
class TidalgtkWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'TidalgtkWindow'

    main_stack = Gtk.Template.Child()
    app_stack = Gtk.Template.Child()
    switchbar_bottom = Gtk.Template.Child()
    player_timebar = Gtk.Template.Child()
    player_reveal = Gtk.Template.Child()
    player_songinfo = Gtk.Template.Child()

    deck_app = Gtk.Template.Child()
    header_switch = Gtk.Template.Child()
    header_stack = Gtk.Template.Child()
    popup_searchbar = Gtk.Template.Child()
    test_player_button = Gtk.Template.Child()

    #Login Page
    log_username = Gtk.Template.Child()
    log_password = Gtk.Template.Child()
    log_button = Gtk.Template.Child()

    #Player UI
    enlarge_player_button = Gtk.Template.Child()
    player_play_button = Gtk.Template.Child()
    player_play_image = Gtk.Template.Child()
    player_cover = Gtk.Template.Child()
    player_title = Gtk.Template.Child()
    player_artist = Gtk.Template.Child()


    #Enlarge player UI
    close_player_button = Gtk.Template.Child()
    playerE_play_button = Gtk.Template.Child()
    playerE_play_image = Gtk.Template.Child()
    playerE_cover = Gtk.Template.Child()
    playerE_title = Gtk.Template.Child()
    playerE_artist = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("check-resize",self.update_scale_interface)
        self.enlarge_player_button.connect("clicked",self.display_player)
        self.close_player_button.connect("clicked",self.display_player)
        self.switchbar_bottom.connect("event",self.display_pages)
        self.header_switch.connect("event",self.display_pages)

        # Init player
        Player(self)

    def update_scale_interface(self, *_):
        if self.header_switch.get_title_visible():
            self.switchbar_bottom.set_reveal(True)
            self.player_timebar.set_visible(False)
            self.player_songinfo.set_hexpand(True)
        else:
            self.switchbar_bottom.set_reveal(False)
            self.player_timebar.set_visible(True)
            self.player_songinfo.set_hexpand(False)

    def display_player(self, *_):
        if self.deck_app.get_visible_child_name() == "app_page":
            self.deck_app.set_visible_child_name("player_page")
        elif self.deck_app.get_visible_child_name() == "player_page":
            self.deck_app.set_visible_child_name("app_page")
            
    def display_pages(self,*_):
        if self.app_stack.get_visible_child_name() == "search_page":
            if self.header_switch.get_title_visible():
                self.header_stack.set_visible_child_name("search")
            else:
                self.popup_searchbar.set_search_mode(True)
        else:
            self.header_stack.set_visible_child_name("main")
            self.popup_searchbar.set_search_mode(False)
