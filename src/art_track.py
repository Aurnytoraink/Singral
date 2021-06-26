# art_track.py
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

from gi.repository import Gtk, Pango, GdkPixbuf

from singral.help_task import TaskHelper

class TrackRow(Gtk.ListBoxRow):
    def __init__(self,track):
        Gtk.ListBoxRow.__init__(self)
        self.track = track

        title = Gtk.Label.new(self.track.title)
        title.set_ellipsize(Pango.EllipsizeMode(3))
        title.set_max_width_chars(30)
        title.set_hexpand(True)
        title.set_xalign(0)
        title.show()

        albumname = Gtk.Label.new(self.track.artist.name)
        albumname.set_ellipsize(Pango.EllipsizeMode(3))
        albumname.set_hexpand(True)
        albumname.set_xalign(0)
        albumname.show()

        artistname = Gtk.Label.new(self.track.artist.name)
        artistname.set_ellipsize(Pango.EllipsizeMode(3))
        artistname.set_hexpand(True)
        artistname.set_xalign(0)
        artistname.show()

        min = int(self.track.duration/60)
        sec = self.track.duration % 60
        if sec < 10:
            sec = "0" + str(sec)
        self.duration = Gtk.Label.new(str(f"{min}:{sec}"))
        self.duration.set_width_chars(4)
        self.duration.show()

        self.cover = Gtk.Image.new()
        self.cover.set_from_icon_name("folder-music-symbolic",35)
        self.cover.show()

        box_name = Gtk.Box.new(Gtk.Orientation(0),0)
        box_name.add(title)
        box_name.add(albumname)
        box_name.add(artistname)
        box_name.set_homogeneous(True)
        box_name.set_hexpand(True)
        box_name.show()

        box = Gtk.Box.new(Gtk.Orientation(0),0)
        box.add(self.cover)
        box.add(box_name)
        box.add(self.duration)
        box.set_spacing(10)
        box.show()
        
        self.add(box)
        self.show()

    def display_cover(self,data):
        loader = GdkPixbuf.PixbufLoader.new()
        loader.write(data)
        loader.close()
        loader = loader.get_pixbuf()
        cover_btn = loader.scale_simple(32,32,GdkPixbuf.InterpType.BILINEAR)
        self.cover.set_from_pixbuf(cover_btn)


class TrackListBox(Gtk.ListBox):
    def __init__(self,player):
        Gtk.ListBox.__init__(self)
        self.player = player
        self.queue = []
        self.get_style_context().add_class("content")
        self.connect("row-activated",self.on_row_clicked)

        self.set_activate_on_single_click(True)
        self.set_selection_mode(Gtk.SelectionMode.NONE)
        self.show()

    def on_row_clicked(self,list,row):
        position = row.get_index()
        TaskHelper().run(self.player.load,self.queue,position)