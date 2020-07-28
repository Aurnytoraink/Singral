import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

class GstPlayer():
    def __init__(self):
        super().__init__()

        Gst.init()

        self.loop = GLib.MainLoop()

        self.player = Gst.ElementFactory.make('playbin3', 'player')
        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message", self.bus_call, self.loop)

    def bus_call(self, bus, message, loop):
        t = message.type
        if t == Gst.MessageType.EOS:
            sys.stdout.write("End-of-stream\n")
            loop.quit()
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            sys.stderr.write("Error: %s: %s\n" % (err, debug))
            loop.quit()
        return True

    def url(self, url):
        self.player.set_property('uri', url)

    def change_state(self, state):
        if state == 2:
            self.player.set_state(Gst.State.PAUSED)
        if state == 0:
            self.player.set_state(Gst.State.NULL)
        if state == 1:
            self.player.set_state(Gst.State.READY)
        if state == 3:
            self.player.set_state(Gst.State.PLAYING)

