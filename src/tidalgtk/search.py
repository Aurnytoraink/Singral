# search.py
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

from gi.repository import Gtk, Handy, GLib
from tidalgtk.api.session import Session
from tidalgtk.art import Artwork
import tidalgtk

class Search(Handy.ApplicationWindow):

    def __init__(self, application):
        super().__init__()
        self.app = application

        self.app.popup_searchbar_entry.connect("search_changed",self.on_search_changed)
        self.timeout = None
        self.query = None
        self.artwork = Artwork()

    def search(self,*_):
        if self.query != "":
            self.app.search_stack.set_visible_child_name("search")
            results = self.app.session.search(self.query)
            self.update_interface(results)
        else:
            self.app.search_stack.set_visible_child_name("label")
            self.clear()

    def clear(self,*_):
        for child in self.app.album_flowbox.get_children():
            self.app.album_flowbox.remove(child)
        for child in self.app.artist_flowbox.get_children():
            self.app.artist_flowbox.remove(child)
        for child in self.app.playlist_flowbox.get_children():
            self.app.playlist_flowbox.remove(child)
        for child in self.app.topsearch_result.get_children():
            self.app.topsearch_result.remove(child)
        self.app.topsearch_box.set_visible(False)
        self.app.track_box.set_visible(False)
        self.app.album_box.set_visible(False)
        self.app.artist_box.set_visible(False)
        self.app.playlist_box.set_visible(False)

    def on_search_changed(self,*_):
        if self.timeout is not None:
            GLib.source_remove(self.timeout)
        self.timeout = GLib.timeout_add(
                500,
                self.on_search_changed_timeout)

    def on_search_changed_timeout(self):
        self.timeout = None
        new_search = self.app.popup_searchbar_entry.get_text()
        if self.query != new_search:
            self.query = new_search
            self.search()


    def update_interface(self, results):
        self.clear()
        #TODO: Add threads
        #Divide results into categories
        if results["tracks"] != []:
            self.app.track_box.set_visible(True)
            for i in range(len(results["tracks"])):
                box = self.artwork.track_boxchild(results["tracks"][i])
                self.app.track_flowbox.insert(box,i)
        else:
            self.app.track_box.set_visible(False)

        #BUG: There is a lag between the album's name and artist's name
        if results["albums"] != []:
            self.app.album_box.set_visible(True)
            for i in range(len(results["albums"])):
                box = self.artwork.album_boxchild(results["albums"][i])
                self.app.album_flowbox.insert(box,i)
        else:
            self.app.album_box.set_visible(False)

        if results["artists"] != []:
            self.app.artist_box.set_visible(True)
            for i in range(len(results["artists"])):
                box = self.artwork.artist_boxchild(results["artists"][i])
                self.app.artist_flowbox.insert(box,i)
        else:
            self.app.artist_box.set_visible(False)

        if results["playlists"] != []:
            self.app.playlist_box.set_visible(True)
            for i in range(len(results["playlists"])):
                box = self.artwork.playlist_boxchild(results["playlists"][i])
                self.app.playlist_flowbox.insert(box,i)

        else:
            self.app.playlist_box.set_visible(False)


    def display_topsearch(self, result):
        if type(result) == tidalgtk.api.artist.Artist:
            box = self.artwork.artist_boxchild(result)
        elif type(result) == tidalgtk.api.album.Album:
            box = self.artwork.album_boxchild(result)
        elif type(result) == tidalgtk.api.media.Track:
            box = self.artwork.track_boxchild(result)
        elif type(result) == tidalgtk.api.playlist.Playlist:
            box = self.artwork.playlist_boxchild(results["playlists"][i])
        self.app.topsearch_result.pack_start(box,False,False,0)
