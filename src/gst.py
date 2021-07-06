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

from gi.repository import Gst, GObject
import gi
gi.require_version('Gst', '1.0')


class GstPlayer(GObject.GObject):
    __gsignals__ = {
        "clock-tick": (GObject.SignalFlags.RUN_FIRST, None, (int, )),
        "stream-finished": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "on_about_to_finish": (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    def __init__(self):
        super().__init__()

        Gst.init(None)

        self.player = Gst.ElementFactory.make('playbin3', 'player')
        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()

        self.bus.connect("message::eos", self.on_bus_eos)
        self.bus.connect("message::error", self.on_bus_error)
        self.bus.connect("message::new-clock", self.new_clock)

        self.player.connect("about-to-finish", self.on_about_to_finish)

        self._state = 0
        self._tick = 0

    def on_bus_error(self, *_):
        return

    def on_bus_eos(self, bus, message):
        self.emit("stream-finished")
        return
        # Envoie un signal
        # Permet de passer à la musique suivante si existe

    def change_track(self, url):
        self.player.set_property('uri', url)

    @GObject.Property(
        type=int, flags=GObject.ParamFlags.READWRITE
        | GObject.ParamFlags.EXPLICIT_NOTIFY)
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

    def on_about_to_finish(self, *_):
        """Send a signal to preload the next song when the current one is about to finish """
        self.emit("on_about_to_finish")

    def _get_duration(self, *_):
        return int(self.player.query_position(Gst.Format.TIME)[1] / 1000000000)

    # TODO Find a way to stop the clock when the song finished
    def new_clock(self, bus, message):
        clock = message.parse_new_clock()
        id = clock.new_periodic_id(0, 1 * Gst.SECOND)
        clock.id_wait_async(id, self._on_clock_tick, None)

    def _on_clock_tick(self, clock, time, id, data):
        self.emit("clock-tick", self._tick)
        self._tick += 1

    def seek(self, position):
        if self._state == 0:
            return False

        self.player.seek_simple(Gst.Format.TIME,
                                Gst.SeekFlags.FLUSH |
                                Gst.SeekFlags.KEY_UNIT,
                                position * 1000000000)
        return True
