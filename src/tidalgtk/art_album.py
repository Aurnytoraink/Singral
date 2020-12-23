# art_album.py
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

from gi.repository import Gtk, Gdk, GdkPixbuf, GLib, Pango
import cairo
from math import pi

class AlbumWidget(Gtk.FlowBoxChild):
    def __init__(self,album):
        Gtk.FlowBoxChild.__init__(self)
        self.album = album

        img = self.album_artwork(album)

        name = Gtk.Label.new()
        name.set_markup(f"<span font_weight='bold'>{GLib.markup_escape_text(album.title)}</span>")
        name.set_ellipsize(Pango.EllipsizeMode(3))
        name.set_max_width_chars(30)
        name.set_justify(Gtk.Justification.CENTER)
        name.show()

        artistname = Gtk.Label.new(album.artist.name)
        artistname.set_ellipsize(Pango.EllipsizeMode(3))
        artistname.set_max_width_chars(30)
        artistname.set_justify(Gtk.Justification.CENTER)
        artistname.show()

        box = Gtk.Box.new(Gtk.Orientation(1),0)
        box.add(img)
        box.add(name)
        box.add(artistname)
        box.set_halign(Gtk.Align.CENTER)
        box.set_valign(Gtk.Align.CENTER)
        box.show()
        
        self.add(box)
        self.show()
        

    def album_artwork(self,album,size=180):
        def rounded(pixbuf):
            surface = cairo.ImageSurface(cairo.Format.ARGB32, size, size)
            ctx = cairo.Context(surface)
            radius = size/10
            ctx.arc(size-radius, radius, radius, -90*(pi/180), 0.0)
            ctx.arc(size-radius, size-radius, radius, 0.0, 90*(pi/180))
            ctx.arc(radius, size-radius, radius, 90*(pi/180), 180*(pi/180))
            ctx.arc(radius, radius, radius, 180*(pi/180), 270*(pi/180))
            ctx.clip()
            ctx.new_path()
            Gdk.cairo_set_source_pixbuf(ctx,pixbuf,0,0)
            ctx.paint()
            return Gdk.pixbuf_get_from_surface(surface, 0, 0, size, size)

        img = Gtk.Image.new()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale('/home/aurnytoraink/Images/Assets/pp.jpg',size,size,True)
        pixbuf = rounded(pixbuf)
        img.set_from_pixbuf(pixbuf)
        img.show()
        return img