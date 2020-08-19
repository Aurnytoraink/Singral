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

from gi.repository import Gtk, Handy, GdkPixbuf, Gdk, GLib, Pango
from tidalgtk.api.session import Session
from tidalgtk.api.download import dl_image
from tidalgtk.art import round_image

class Search(Handy.ApplicationWindow):

    def __init__(self, application):
        super().__init__()
        self.app = application

        self.app.popup_searchbar_entry.connect("search_changed",self.on_search_changed)
        self.timeout = None
        self.query = None

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
        if results["top_hit"] != None:
            self.app.topsearch_box.set_visible(True)
            self.display_topsearch(results["top_hit"])
        else:
            self.app.topsearch_box.set_visible(False)

        if results["tracks"] != []:
            self.app.track_box.set_visible(True)
            for i in range(len(results["tracks"])):
                self.display_track(results["tracks"][i], i)
        else:
            self.app.track_box.set_visible(False)

        if results["albums"] != []:
            self.app.album_box.set_visible(True)
            for i in range(len(results["albums"])):
                self.display_album(results["albums"][i],results["albums"][i].artist, i)
        else:
            self.app.album_box.set_visible(False)

        if results["artists"] != []:
            self.app.artist_box.set_visible(True)
            for i in range(len(results["artists"])):
                self.display_artist(results["artists"][i], i)
        else:
            self.app.artist_box.set_visible(False)

        if results["playlists"] != []:
            self.app.playlist_box.set_visible(True)
            for i in range(len(results["playlists"])):
                self.display_playlist(results["playlists"][i], i)
        else:
            self.app.playlist_box.set_visible(False)


    def display_topsearch(self, result):
        return

    def display_track(self, result, i):
        return

    def display_album(self, result, artist, i):
        #BUG: There is a lag between the album's name and artist's name
        #TODO: In album module (and others), in the image(), make it return a premade GdkPixbuf
        img = Gtk.Image.new()
        dl_image(result.id,'album',result.image(320))
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale('/var/cache/files/covers/album_{}.jpg'.format(result.id),200,200,True)
        img.set_from_pixbuf(pixbuf)
        name = Gtk.Label.new()
        name.set_markup(
            "<b>" + GLib.markup_escape_text(result.name) + "</b>")
        name.set_ellipsize(Pango.EllipsizeMode(3))
        artists = Gtk.Label.new(artist.name)
        artists.set_ellipsize(Pango.EllipsizeMode(3))
        box = Gtk.Box.new(Gtk.Orientation(1),0)
        box.pack_start(img,False,False,0)
        box.pack_start(name,False,False,0)
        box.pack_start(artists,False,False,0)
        self.app.album_flowbox.insert(box,i)
        box.set_visible(True)
        name.set_visible(True)
        artists.set_visible(True)
        img.set_visible(True)

    def display_artist(self, result, i):
        #BUG: Bug with the artist Adele
        name = Gtk.Label.new()
        name.set_markup(
            "<b>" + GLib.markup_escape_text(result.name) + "</b>")
        name.set_ellipsize(Pango.EllipsizeMode(3))
        box = Gtk.Box.new(Gtk.Orientation(1),0)

        # If the artist doesn't have a picture (for ex: 6338535)
        if result.image(320) != None:
            dl_image(result.id,'artist',result.image(320))
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale('/var/cache/files/covers/artist_{}.jpg'.format(result.id),200,200,True)
            pixbuf = round_image(pixbuf)
            img = Gtk.Image.new()
            img.set_from_pixbuf(pixbuf)
            box.pack_start(img,False,False,0)
            img.set_visible(True)
        else:
            avatar = Handy.Avatar.new(200,result.name,True)
            box.pack_start(avatar,False,False,0)
            avatar.set_visible(True)

        box.pack_start(name,False,False,0)
        self.app.artist_flowbox.insert(box,i)
        box.set_visible(True)
        name.set_visible(True)


    def display_playlist(self, result, i):
        img = Gtk.Image.new()
        dl_image(result.id,'playlist',result.image(320))
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale('/var/cache/files/covers/playlist_{}.jpg'.format(result.id),200,200,True)
        img.set_from_pixbuf(pixbuf)
        name = Gtk.Label.new()
        name.set_markup(
            "<b>" + GLib.markup_escape_text(result.name) + "</b>")
        name.set_ellipsize(Pango.EllipsizeMode(3))
        box = Gtk.Box.new(Gtk.Orientation(1),0)
        box.pack_start(img,False,False,0)
        box.pack_start(name,False,False,0)
        self.app.playlist_flowbox.insert(box,i)
        box.set_visible(True)
        name.set_visible(True)
        img.set_visible(True)          
