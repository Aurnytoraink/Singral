# library.py
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
from tidalgtk.art import Artwork

class Favs(Handy.ApplicationWindow):
    def __init__(self, application):
        super().__init__()

        self.app = application

    def show_albums(self,result):
        self.app.fav_stack.set_visible_child_name("fav_albums_page")
        for child in self.app.fav_albums_flowbox.get_children():
            self.app.fav_albums_flowbox.remove(child)
        for i in range(len(result)):
            box = Artwork().album_boxchild(result[i])
            self.app.fav_albums_flowbox.insert(box,i)

    def show_artists(self,result):
        self.app.fav_stack.set_visible_child_name("fav_artists_page")
        for child in self.app.fav_artists_flowbox.get_children():
            self.app.fav_artists_flowbox.remove(child)
        for i in range(len(result)):
            box = Artwork().artist_boxchild(result[i])
            self.app.fav_artists_flowbox.insert(box,i)

    def show_tracks(self,result):
        self.app.fav_stack.set_visible_child_name("fav_tracks_page")
        for child in self.app.fav_tracks_flowbox.get_children():
            self.app.fav_tracks_flowbox.remove(child)
        for i in range(len(result)):
            box = Artwork().track_boxchild(result[i])
            self.app.fav_tracks_flowbox.insert(box,i)
