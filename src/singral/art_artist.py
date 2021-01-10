# art_artist.py
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

from gi.repository import Gtk, Handy, Gdk, GdkPixbuf, Pango
from singral.help_task import TaskHelper

class ArtistRow(Gtk.ListBoxRow):
    def __init__(self,artist):
        Gtk.ListBoxRow.__init__(self)
        self.artist = artist

        artist_name = Gtk.Label.new()
        artist_name.set_markup(f"<span font_weight='bold'>{artist.name}</span>")
        # artist_name.set_ellipsize(Pango.EllipsizeMode(3))
        artist_name.set_max_width_chars(23)
        artist_name.set_justify(Gtk.Justification.CENTER)
        artist_name.show()

        self.cover = Handy.Avatar.new(35,artist.name,True)
        self.cover.show()

        box = Gtk.Box.new(Gtk.Orientation(0),0)
        box.add(self.cover)
        box.add(artist_name)
        box.set_spacing(10)
        box.show()
        
        self.add(box)
        self.show()

    def display_cover(self,data,size=35):
        loader = GdkPixbuf.PixbufLoader.new()
        loader.write(data)
        loader.close()
        loader = loader.get_pixbuf()
        loader = loader.scale_simple(size,size,GdkPixbuf.InterpType.BILINEAR)
        self.cover.set_image_load_func(Handy.AvatarImageLoadFunc(size,loader))

class ArtistViewPage(Gtk.Box):
    def __init__(self,artist):
        Gtk.Box.__init__(self)
        self.artist = artist

        self.cover = Handy.Avatar.new(112,artist.name,True)
        self.cover.show()

        artist_name = Gtk.Label.new()
        artist_name.set_markup(f"<span font_weight='bold' font_size='x-large'>{artist.name}</span>")
        artist_name.set_ellipsize(Pango.EllipsizeMode(3))
        artist_name.set_max_width_chars(25)
        artist_name.set_xalign(0)
        artist_name.show()

        #TODO Utiliser un Gtk.TextView plutôt
        self.artist_bio = Gtk.Label.new()
        self.artist_bio.set_xalign(0)
        self.artist_bio.set_justify(Gtk.Justification.FILL)
        self.artist_bio.show()
        
        viewport = Gtk.Viewport.new()
        viewport.add(self.artist_bio)
        viewport.show()
        scrollpage = Gtk.ScrolledWindow.new()
        scrollpage.add(viewport)
        scrollpage.show()

        artist_label = Gtk.Box.new(Gtk.Orientation(1),0)
        artist_label.add(artist_name)
        artist_label.add(scrollpage)
        artist_label.set_spacing(10)
        artist_label.show()

        artist_box = Gtk.Box.new(Gtk.Orientation(0),0)
        artist_box.add(self.cover)
        artist_box.add(artist_label)
        artist_box.set_spacing(10)
        artist_box.set_hexpand(True)
        artist_box.show()

        #Top Tracks
        track_label = Gtk.Label.new()
        track_label.set_markup("<span font_weight='bold' font_size='x-large'>Top Tracks</span>")
        track_label.set_xalign(0)
        track_label.show()

        track_box = Gtk.Box.new(Gtk.Orientation(1),0)
        track_box.add(track_label)
        track_box.set_spacing(3)
        track_box.set_vexpand(True)
        track_box.show()

        #Albums
        album_label = Gtk.Label.new()
        album_label.set_markup("<span font_weight='bold' font_size='x-large'>Albums</span>")
        album_label.set_xalign(0)
        album_label.show()

        album_box = Gtk.Box.new(Gtk.Orientation(1),0)
        album_box.add(album_label)
        album_box.set_spacing(3)
        album_box.set_vexpand(True)
        album_box.show()

        # box = Gtk.Box.new(Gtk.Orientation(1),0)
        self.add(artist_box)
        self.add(track_box)
        self.add(album_box)
        self.set_spacing(30)
        self.set_orientation(Gtk.Orientation(1))
        self.show()

    def display_artist_info(self,artist):
        self.artist = artist
        self.artist_bio.set_text(self.artist.bio)
        return


class ArtistListBox(Gtk.ListBox):
    def __init__(self,app):
        self.app = app
        Gtk.ListBox.__init__(self)
        self.connect("row-selected",self.on_row_selected)
        self.set_activate_on_single_click(True)
        self.set_selection_mode(Gtk.SelectionMode.BROWSE)
        self.show()

    def on_row_selected(self,list,row):
        for child in self.app.artist_viewpage.get_children(): child.destroy()
        viewpage = ArtistViewPage(row.artist)
        self.app.artist_viewpage.add(viewpage)
        TaskHelper().run(self.app.session.get_artist,viewpage.artist.id,callback=(viewpage.display_artist_info,))