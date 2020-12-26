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

class ArtistRow(Gtk.ListBoxRow):
    def __init__(self,artist):
        Gtk.ListBoxRow.__init__(self)
        self.artist = artist

        artistname = Gtk.Label.new()
        artistname.set_markup(f"<span font_weight='bold'>{artist.name}</span>")
        # artistname.set_ellipsize(Pango.EllipsizeMode(3))
        artistname.set_max_width_chars(23)
        artistname.set_justify(Gtk.Justification.CENTER)
        artistname.show()

        self.cover = Handy.Avatar.new(35,artist.name,True)
        self.cover.show()

        box = Gtk.Box.new(Gtk.Orientation(0),0)
        box.add(self.cover)
        box.add(artistname)
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
        self.set_image_load_func(HdyAvatarImageLoadFunc(size,loader))

class ArtistListBox(Gtk.ListBox):
    def __init__(self):
        Gtk.ListBox.__init__(self)
        self.connect("row-selected",self.on_row_selected)
        self.set_activate_on_single_click(True)
        self.set_selection_mode(Gtk.SelectionMode.BROWSE)
        self.show()

    def on_row_selected(self,list,row):
        print(row.artist.name)
    #     position = row.get_index()
    #     TaskHelper().run(self.player.load,self.queue,position)