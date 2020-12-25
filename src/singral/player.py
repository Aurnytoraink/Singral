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

import random

from gi.repository import Gtk, Handy, GdkPixbuf, Gdk, GLib

from singral.gst import GstPlayer
from singral.help_task import TaskHelper
from singral.help_artwork import get_cover_from_album

class Player(Handy.ApplicationWindow):
    def __init__(self, application, session):
        super().__init__()

        # Init GstPlayer
        self.gst = GstPlayer()
        self.gst.state = 0

        self.session = session

        self.app = application
        self.app.connect("delete-event",self.close_win)

        self.app.player_play_button.connect("clicked",self.play_pause)
        self.app.playerE_play_button.connect("clicked",self.play_pause)
        self.app.player_prev_button.connect("clicked",self.prev)
        self.app.playerE_prev_button.connect("clicked",self.prev)
        self.app.player_next_button.connect("clicked",self.next)
        self.app.playerE_next_button.connect("clicked",self.next)
        self.app.player_duration_scale.connect("button-release-event",self.set_seek)
        self.app.playerE_duration_scale.connect("button-release-event",self.set_seek)
        self.app.like_button.connect("clicked",self.update_like)
        self.app.playerE_repeat_button.connect("clicked",self.update_repeat)
        self.app.playerE_shuffle_button.connect("clicked",self.update_shuffle)

        self.gst.connect("clock-tick",self.update_duration)
        self.gst.connect("stream-finished",self.next)
        self.gst.connect("on_about_to_finish",self.preload)

        #Repeat(0: Disabled, 1:Playlist, 2:Current song)
        self.repeat_state = 0
        self.shuffle_state = False

        self.queue = []
        #The saved queue is used when you user want to disable shuffle and returns to the original queues
        self.saved_queue = []
        self.current_song = 0

    def preload(self,*_):
        TaskHelper().run(self.session.get_streamable_url,self.queue[self.current_song+1])

    def load(self,queue,position):
        self.queue = queue
        self.current_song = position
        TaskHelper().run(self.play,self.queue[self.current_song],callback=(self.update_interface,))

    def play(self, track):
        self.gst.state = 0
        self.url = self.session.get_streamable_url(track)
        self.gst.change_track(self.url)
        self.gst.state = 3
        return track

    def update_interface(self,track):
        def display_cover(data,self):
            try:
                loader = GdkPixbuf.PixbufLoader.new()
                loader.write(data)
                loader.close()
                loader = loader.get_pixbuf()
                cover_btn = loader.scale_simple(32,32,GdkPixbuf.InterpType.BILINEAR)
                cover_enlarge_player = loader.scale_simple(316,316,GdkPixbuf.InterpType.BILINEAR)
                self.app.player_cover.set_from_pixbuf(cover_btn)
                self.app.playerE_cover.set_from_pixbuf(cover_enlarge_player)
            except:
                self.app.player_cover.set_from_icon_name("folder-music-symbolic",32)
                self.app.playerE_cover.set_from_icon_name("folder-music-symbolic",316)

        #Display songs info
        self.app.player_play_image.set_from_icon_name("media-playback-pause-symbolic",Gtk.IconSize.BUTTON)
        self.app.playerE_play_image.set_from_icon_name("media-playback-pause-symbolic",-1)
        self.app.player_title.set_text(track.title)
        self.app.playerE_title.set_text(track.title)
        self.app.player_artist.set_text(track.artist.name)
        self.app.playerE_artist.set_text(track.artist.name)
        min = int(track.duration/60)
        sec = track.duration % 60
        if sec < 10:
            sec = "0" + str(sec)
        self.app.player_total_duration.set_text(f"{min}:{sec}")
        self.app.playerE_total_duration.set_text(f"{min}:{sec}")

        #Set duration scale
        self.app.duration_scale.set_upper(float(track.duration))
        self.app.duration_scale.set_value(self.app.duration_scale.props.lower)

        #Display cover (if avaible)
        if track.cover is not None:
            TaskHelper().run(get_cover_from_album,track,self.session,callback=(display_cover,self))
        else:
            self.app.player_cover.set_from_icon_name("folder-music-symbolic",32)
            self.app.playerE_cover.set_from_icon_name("folder-music-symbolic",316)

        #Display like statue:
        # if track.like:
        #     self.app.like_button_img.set_from_icon_name("heart-filled-symbolic",Gtk.IconSize.BUTTON)
        # else:
        #     self.app.like_button_img.set_from_icon_name("heart-outline-thin-symbolic",Gtk.IconSize.BUTTON)

        self.app.player_reveal.set_reveal_child(True)
        self.update_queue()

    def play_pause(self,*_):
        if self.gst._state == 3:
            self.gst.state = 2
            self.app.player_play_image.set_from_icon_name("media-playback-start-symbolic",Gtk.IconSize.BUTTON)
            self.app.playerE_play_image.set_from_icon_name("media-playback-start-symbolic",-1)
        elif self.gst._state == 2:
            self.gst.state = 3
            self.app.player_play_image.set_from_icon_name("media-playback-pause-symbolic",Gtk.IconSize.BUTTON)
            self.app.playerE_play_image.set_from_icon_name("media-playback-pause-symbolic",-1)
        elif self.gst._state == 0:
            self.gst.state = 3
            self.app.player_play_image.set_from_icon_name("media-playback-pause-symbolic",Gtk.IconSize.BUTTON)
            self.app.playerE_play_image.set_from_icon_name("media-playback-pause-symbolic",-1)

    def stop(self):
        self.app.player_play_image.set_from_icon_name("media-playback-start-symbolic",Gtk.IconSize.BUTTON)
        self.app.playerE_play_image.set_from_icon_name("media-playback-start-symbolic",-1)

    def has_next(self):
        if self.current_song >= (len(self.queue) - 1):
            return False
        return True

    def next(self,*_):
        if self.repeat_state == 2:
            TaskHelper().run(self.play,self.queue[self.current_song],callback=(self.update_interface,))
            return

        if self.has_next():
            self.current_song += 1
            TaskHelper().run(self.play,self.queue[self.current_song],callback=(self.update_interface,))
        else:
            if self.repeat_state == 1:
                self.current_song = 0
                TaskHelper().run(self.play,self.queue[self.current_song],callback=(self.update_interface,))
            else:
                self.stop()

    def prev(self,*_):
        if self.repeat_state == 2 or self.current_song == 0 or self.gst._get_duration() > 3:
            TaskHelper().run(self.play,self.queue[self.current_song],callback=(self.update_interface,))
            return

        self.current_song -= 1
        TaskHelper().run(self.play,self.queue[self.current_song],callback=(self.update_interface,))

    #Stop music when user closes window
    def close_win(self,*_):
        self.gst.state = 0

    def update_duration(self,*_):
        duration = self.gst._get_duration()
        minutes = int(duration/60)
        secondes = duration % 60
        if secondes < 10:
            secondes = "0" + str(secondes)
        self.app.player_actual_duration.set_text("{0}:{1}".format(str(minutes),str(secondes)))
        self.app.playerE_actual_duration.set_text("{0}:{1}".format(str(minutes),str(secondes)))
        self.app.duration_scale.set_value(self.gst._get_duration())

    def update_queue(self,*_):
        if self.current_song >= (len(self.queue) - 1) and self.repeat_state == 0:
            self.app.player_next_button.set_sensitive(False)
            self.app.playerE_next_button.set_sensitive(False)
        else:
            self.app.player_next_button.set_sensitive(True)
            self.app.playerE_next_button.set_sensitive(True)

    def update_like(self,*_):
        if self.queue[self.current_song].like:
            self.queue[self.current_song].like = False
            self.app.like_button_img.set_from_icon_name("heart-outline-thin-symbolic",Gtk.IconSize.BUTTON)
        else:
            self.queue[self.current_song].like = True
            self.app.like_button_img.set_from_icon_name("heart-filled-symbolic",Gtk.IconSize.BUTTON)

    def update_repeat(self,*_):
        if self.repeat_state == 2:
            self.repeat_state = 0
        else:
            self.repeat_state += 1
        self.update_queue()

        #Update interface
        if self.repeat_state == 0:
            self.app.repeat_state_img.set_from_icon_name("media-playlist-norepeat-symbolic",Gtk.IconSize.BUTTON)
        if self.repeat_state == 1:
            self.app.repeat_state_img.set_from_icon_name("media-playlist-repeat-symbolic",Gtk.IconSize.BUTTON)
        if self.repeat_state == 2:
            self.app.repeat_state_img.set_from_icon_name("media-playlist-repeat-song-symbolic",Gtk.IconSize.BUTTON)

    def update_shuffle(self,*_):
        if self.shuffle_state is False:
            self.shuffle_state = True
            current_song = self.queue[self.current_song]
            self.saved_queue = self.queue.copy()
            random.shuffle(self.queue)
            self.queue.remove(current_song)
            self.queue.insert(0,current_song)
            self.current_song = 0
            self.app.shuffle_state_img.set_from_icon_name("media-playlist-shuffle-symbolic",Gtk.IconSize.BUTTON)
        else:
            self.shuffle_state = False
            current_song = self.queue[self.current_song]
            self.queue = self.saved_queue.copy()
            self.current_song = self.queue.index(current_song)
            self.app.shuffle_state_img.set_from_icon_name("media-playlist-noshuffle-symbolic",Gtk.IconSize.BUTTON)
        self.update_queue()


    #When user change the current duration
    def set_seek(self, *args):
        value = int(self.app.duration_scale.get_value())
        if self.gst.seek(value):
            self.app.duration_scale.set_value(self.gst._get_duration())
