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

from gi.repository import Gtk, Pango

from tidalgtk.help_task import TaskHelper

class TrackRow(Gtk.ListBoxRow):
    def __init__(self,track):
        Gtk.ListBoxRow.__init__(self)
        self.track = track

        title = Gtk.Label.new(self.track.title)
        title.set_ellipsize(Pango.EllipsizeMode(3))
        title.set_max_width_chars(30)
        # title.set_justify(Gtk.Justification.CENTER)
        title.set_hexpand(True)
        title.set_xalign(0)
        title.show()

        albumname = Gtk.Label.new(self.track.artist.name)
        albumname.set_ellipsize(Pango.EllipsizeMode(3))
        # albumname.set_max_width_chars(30)
        # albumname.set_justify(Gtk.Justification.CENTER)
        albumname.set_hexpand(True)
        albumname.set_xalign(0)
        albumname.show()

        artistname = Gtk.Label.new(self.track.artist.name)
        artistname.set_ellipsize(Pango.EllipsizeMode(3))
        # artistname.set_max_width_chars(30)
        # artistname.set_justify(Gtk.Justification.CENTER)
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

        box_name = Gtk.Box.new(Gtk.Orientation(0),0)
        box_name.add(title)
        box_name.add(albumname)
        box_name.add(artistname)
        box_name.set_homogeneous(True)
        box_name.set_hexpand(True)
        box_name.show()

        box = Gtk.Box.new(Gtk.Orientation(0),0)
        box.add(box_name)
        box.add(self.duration)
        box.show()
        
        self.add(box)
        self.show()

    def update_duration(self,*_):
        min = int(self.track.duration/60)
        sec = self.track.duration % 60
        if sec < 10:
            sec = "0" + str(sec)
        self.duration.set_text(str(f"{min}:{sec}"))


class TrackListBox(Gtk.ListBox):
    # def __init__(self,player):
    def __init__(self):
        Gtk.ListBox.__init__(self)
        # self.player = player
        self.queue = []
        self.get_style_context().add_class("content")
        # self.connect("row-activated",self.on_row_clicked)

        self.set_activate_on_single_click(True)
        self.set_selection_mode(Gtk.SelectionMode.NONE)
        self.show()

    # def on_row_clicked(self,list,row):
    #     position = row.get_index()
    #     TaskHelper().run(self.player.load,self.queue,position)