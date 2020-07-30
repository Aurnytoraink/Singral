# player.py
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

from gi.repository import Gtk, Handy, GdkPixbuf, Gdk
from tidalgtk.gst import GstPlayer

class Player(Handy.ApplicationWindow):
    def __init__(self, application):
        super().__init__()

        # Init GstPlayer
        self.player = GstPlayer()
        self.player.state = 0

        self.app = application
        self.app.player_play_button.connect("clicked",self.play_pause)
        self.app.playerE_play_button.connect("clicked",self.play_pause)
        self.app.connect("delete-event",self.close_win)
        self.app.test_player_button.connect("clicked",self.test)
        self.app.test_stop_button.connect("clicked",self.stop)

        self.player.connect("clock-tick",self.update_duration)
        self.player.connect("stream-finished",self.stop)

    def play_pause(self,*_):
        if self.player._state == 3:
            self.player.state = 2
            self.app.player_play_image.set_from_icon_name("media-playback-start-symbolic",Gtk.IconSize.BUTTON)
            self.app.playerE_play_image.set_from_icon_name("media-playback-start-symbolic",-1)
        elif self.player._state == 2:
            self.player.state = 3
            self.app.player_play_image.set_from_icon_name("media-playback-pause-symbolic",Gtk.IconSize.BUTTON)
            self.app.playerE_play_image.set_from_icon_name("media-playback-pause-symbolic",-1)
        elif self.player._state == 0:
            self.player.state = 3
            self.app.player_play_image.set_from_icon_name("media-playback-pause-symbolic",Gtk.IconSize.BUTTON)
            self.app.playerE_play_image.set_from_icon_name("media-playback-pause-symbolic",-1)

    def play(self, track, title, artist, duration, cover=None):
        self.player.state = 0
        self.player.change_track(track)
        self.player.state = 3
        self.app.player_play_image.set_from_icon_name("media-playback-pause-symbolic",Gtk.IconSize.BUTTON)
        self.app.playerE_play_image.set_from_icon_name("media-playback-pause-symbolic",-1)
        self.app.player_title.set_text(title)
        self.app.playerE_title.set_text(title)
        self.app.player_artist.set_text(artist)
        self.app.playerE_artist.set_text(artist)
        minutes = int(duration/60)
        secondes = duration % 60
        if secondes < 10:
            secondes = "0" + str(secondes)
        self.app.player_total_duration.set_text("{0}:{1}".format(str(minutes),str(secondes)))
        self.app.playerE_total_duration.set_text("{0}:{1}".format(str(minutes),str(secondes)))
        self._current_duration = self.app.duration_scale.props.lower
        self.app.duration_scale.set_upper(float(duration))
        self.app.duration_scale.set_value(self.app.duration_scale.props.lower)

        if cover:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(cover,32,32,True)
            self.app.player_cover.set_from_pixbuf(pixbuf)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(cover,316,316,True)
            self.app.playerE_cover.set_from_pixbuf(pixbuf)
        else:
            self.app.player_cover.set_from_icon_name("folder-music-symbolic",32)
            self.app.playerE_cover.set_from_icon_name("folder-music-symbolic",316)

    def stop(self,*_):
        print("prou ahah")
        self.player.state = 0
        self.app.player_actual_duration.set_text("0:00")
        self.app.playerE_actual_duration.set_text("0:00")
        self.app.player_play_image.set_from_icon_name("media-playback-start-symbolic",Gtk.IconSize.BUTTON)
        self.app.playerE_play_image.set_from_icon_name("media-playback-start-symbolic",-1)


    # Allow app to be totally close
    def close_win(self,*_):
        self.player.state = 0

    # Only here for tests
    def test(self,*_):
        filechooser = Gtk.FileChooserDialog("Open File",
                                           self.app,
                                           Gtk.FileChooserAction.OPEN,
                                           ("_Cancel", Gtk.ResponseType.CANCEL,
                                            "_Open", Gtk.ResponseType.OK)
                                           )
        response = filechooser.run()
        if response == Gtk.ResponseType.OK:
            filename = filechooser.get_uri()
            self.play(filename, "I Feel Love","N U I T",240,"/home/aurnytoraink/Musique/N U I T/Enjoy the Night/Enjoy the Night.jpg")
            self.app.player_reveal.set_reveal_child(True)
        filechooser.destroy()
        
    def update_duration(self,*_):
        self._current_duration += 1.0
        duration = self.player._get_duration()
        minutes = int(duration/60)
        secondes = duration % 60
        if secondes < 10:
            secondes = "0" + str(secondes)
        self.app.player_actual_duration.set_text("{0}:{1}".format(str(minutes),str(secondes)))
        self.app.playerE_actual_duration.set_text("{0}:{1}".format(str(minutes),str(secondes)))
        self.app.duration_scale.set_value(self._current_duration)
