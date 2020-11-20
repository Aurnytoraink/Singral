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

import threading
from gi.repository import Gtk, Handy, GObject, GLib, Gdk
from tidalgtk.player import Player
from tidalgtk.search import Search
from tidalgtk.api.session import Session

@Gtk.Template(resource_path='/com/github/Aurnytoraink/TidalGTK/ui/window.ui')
class TidalgtkWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'TidalgtkWindow'

    main_stack = Gtk.Template.Child()
    app_stack = Gtk.Template.Child()
    deck_app = Gtk.Template.Child()
    header_switch = Gtk.Template.Child()
    switchbar_bottom = Gtk.Template.Child()

    #Login Page
    log_username = Gtk.Template.Child()
    log_password = Gtk.Template.Child()
    log_button = Gtk.Template.Child()
    log_error_reveal = Gtk.Template.Child()
    log_error_label = Gtk.Template.Child()
    log_button_stack = Gtk.Template.Child()
    create_account_btn = Gtk.Template.Child()
    log_forget_reveal = Gtk.Template.Child()
    forget_pwd_btn = Gtk.Template.Child()

    #Discover Page
    welcome_label = Gtk.Template.Child()

    #Search Page
    search_stack = Gtk.Template.Child()
    popup_searchbar = Gtk.Template.Child()
    popup_searchbar_entry = Gtk.Template.Child()
    topsearch_box = Gtk.Template.Child()
    topsearch_result = Gtk.Template.Child()
    album_flowbox = Gtk.Template.Child()
    album_box = Gtk.Template.Child()
    artist_flowbox = Gtk.Template.Child()
    artist_box = Gtk.Template.Child()
    track_box = Gtk.Template.Child()
    track_flowbox = Gtk.Template.Child()
    playlist_flowbox = Gtk.Template.Child()
    playlist_box = Gtk.Template.Child()

    #Favorites Page
    fav_listbox = Gtk.Template.Child()
    fav_stack = Gtk.Template.Child()
    fav_albums_flowbox = Gtk.Template.Child()
    fav_artists_flowbox = Gtk.Template.Child()
    fav_tracks_listbox = Gtk.Template.Child()

    #Player UI
    duration_scale = Gtk.Template.Child()
    enlarge_player_button = Gtk.Template.Child()
    player_actual_duration = Gtk.Template.Child()
    player_total_duration = Gtk.Template.Child()
    player_duration_scale = Gtk.Template.Child()
    player_play_button = Gtk.Template.Child()
    player_play_image = Gtk.Template.Child()
    player_prev_button = Gtk.Template.Child()
    player_next_button = Gtk.Template.Child()
    player_cover = Gtk.Template.Child()
    player_title = Gtk.Template.Child()
    player_artist = Gtk.Template.Child()
    player_timebar = Gtk.Template.Child()
    player_reveal = Gtk.Template.Child()
    player_songinfo = Gtk.Template.Child()

    #Enlarge player UI
    playerE_actual_duration = Gtk.Template.Child()
    playerE_total_duration = Gtk.Template.Child()
    playerE_duration_scale = Gtk.Template.Child()
    close_player_button = Gtk.Template.Child()
    playerE_play_button = Gtk.Template.Child()
    playerE_play_image = Gtk.Template.Child()
    playerE_prev_button = Gtk.Template.Child()
    playerE_next_button = Gtk.Template.Child()
    playerE_cover = Gtk.Template.Child()
    playerE_title = Gtk.Template.Child()
    playerE_artist = Gtk.Template.Child()
    playerE_shuffle_button = Gtk.Template.Child()
    shuffle_state_img = Gtk.Template.Child()
    playerE_repeat_button = Gtk.Template.Child()
    repeat_state_img = Gtk.Template.Child()
    like_button_img = Gtk.Template.Child()
    like_button = Gtk.Template.Child()

    # TEST ONLY
    test_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("check-resize",self.update_scale_interface)
        self.enlarge_player_button.connect("clicked",self.display_player)
        self.close_player_button.connect("clicked",self.display_player)
        self.log_button.connect("clicked",self.login_username)
        self.log_username.connect("changed",self.update_login_page)
        self.log_password.connect("changed",self.update_login_page)
        self.create_account_btn.connect("clicked",self.create_account)
        self.forget_pwd_btn.connect("clicked",self.forget_pwd)
        # TEST ONLY
        self.test_button.connect("clicked",self.logoff)

        # Init player
        Player(self)

        #Init API
        Search(self)
        self.session = Session(self)

        #Setup CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource('/com/github/Aurnytoraink/TidalGTK/css/style.css')
        Gtk.StyleContext.add_provider_for_screen(
            self.get_screen(), css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.playerE_play_button.get_style_context().add_class("pause_button")
        self.playerE_next_button.get_style_context().add_class("next_button")
        self.enlarge_player_button.get_style_context().add_class("enlarge_button")

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

    def login_username(self,*_):
        self.log_error_reveal.set_reveal_child(False)
        self.log_button.set_sensitive(False)
        self.log_button_stack.set_visible_child_name("try")
        threading.Thread(target=self.session.login,args=(self.log_username.get_text(), self.log_password.get_text(),)).start()

    def on_login_sucess(self):
        self.welcome_label.set_text(f"Welcome, {self.session.username}")
        self.main_stack.set_visible_child_name("app_page")
        self.log_username.set_text("")
        self.log_password.set_text("")
        self.log_button.set_sensitive(True)
        self.log_button_stack.set_visible_child_name("icon")

    def on_login_unsucess(self,*_):
        self.log_button.set_sensitive(True)
        self.log_button_stack.set_visible_child_name("icon")
        self.log_error_label.set_text("Wrong email/password")
        self.log_error_reveal.set_reveal_child(True)
        self.log_forget_reveal.set_reveal_child(True)

    def on_login_error(self,*_):
        self.log_button.set_sensitive(True)
        self.log_button_stack.set_visible_child_name("icon")
        self.log_error_label.set_text("A internal error occured")
        self.log_error_reveal.set_reveal_child(True)

    def update_login_page(self,*_):
        self.log_error_reveal.set_reveal_child(False)
        self.log_forget_reveal.set_reveal_child(False)

    def logoff(self,*_):
        self.session.logoff()
        self.main_stack.set_visible_child_name("login_page")
        for child in self.fav_albums_flowbox.get_children():
            self.fav_albums_flowbox.remove(child)
        for child in self.fav_artists_flowbox.get_children():
            self.fav_artists_flowbox.remove(child)
        for child in self.fav_tracks_flowbox.get_children():
            self.fav_tracks_flowbox.remove(child)
        for child in self.fav_tracks_listbox.get_children():
            self.fav_tracks_listbox.remove(child)

    def create_account(self,*_):
        Gtk.show_uri_on_window(self,"https://www.qobuz.com",Gdk.CURRENT_TIME)

    def forget_pwd(self,*_):
        Gtk.show_uri_on_window(self,"https://www.qobuz.com/reset-password",Gdk.CURRENT_TIME)

    # Library Page #

    def get_fav_albums(self,*_):
        threading.Thread(target=self.session.get_userfav_albums).start()

    def get_fav_artists(self,*_):
        threading.Thread(target=self.session.get_userfav_artists).start()

    def get_fav_tracks(self,*_):
        threading.Thread(target=self.session.get_userfav_tracks).start()

    def get_fav_playlists(self,*_):
        threading.Thread(target=self.session.get_userfav_playlists).start()
