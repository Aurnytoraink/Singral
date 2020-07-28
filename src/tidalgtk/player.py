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

from gi.repository import Gtk, Handy
class Player(Handy.ApplicationWindow):
    def __init__(self, application):
        super().__init__()
        self.app = application
        self.app.player_play_button.connect("clicked",self.player_pause)
        self.app.playerE_play_button.connect("clicked",self.player_pause)

    def player_pause(self,*_):
        if self.app.player._state == 3:
            self.app.player.state = 2
            self.app.player_button_image.set_from_icon_name("media-playback-start-symbolic",Gtk.IconSize.BUTTON)
            self.app.playerE_button_image.set_from_icon_name("media-playback-start-symbolic",-1)
        elif self.app.player._state == 2:
            self.app.player.state = 3
            self.app.player_button_image.set_from_icon_name("media-playback-pause-symbolic",Gtk.IconSize.BUTTON)
            self.app.playerE_button_image.set_from_icon_name("media-playback-pause-symbolic",-1)
