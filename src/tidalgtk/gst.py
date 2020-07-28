# gst.py
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

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

class GstPlayer():
    def __init__(self):
        super().__init__()

        Gst.init(None)

        self.player = Gst.ElementFactory.make('playbin3', 'player')
        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()

        self.bus.connect("message::eos", self.on_bus_eos)
        self.bus.connect("message::error", self.on_bus_error)

        self.player.connect("about-to-finish", self.on_stream_about_to_finish)

        self._state = 0


    def on_bus_error(self,*_):
        return

    def on_bus_eos(self,*_):
        print("Finished")

    def change_track(self, url):
        self.player.set_property('uri', url)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if state == 2:
            self.player.set_state(Gst.State.PAUSED)
            self._state = 2
        elif state == 0:
            self.player.set_state(Gst.State.NULL)
            self._state = 0
        elif state == 1:
            self.player.set_state(Gst.State.READY)
            self._state = 1
        elif state == 3:
            self.player.set_state(Gst.State.PLAYING)
            self._state = 3

    def on_stream_about_to_finish(self, *_):
        print("finish")
        # Générer un signal qui sera envoyer à player.py

