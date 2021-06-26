# log_background.py
#
# Copyright 2020 Gabriele Musco
# https://gabmus.org/posts/create_an_auto-resizing_image_widget_with_gtk3_and_python/
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

from gi.repository import Gtk, GdkPixbuf, Gdk


class LogBackground(Gtk.DrawingArea):
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_resource(self.path)
        self.img_surface = Gdk.cairo_surface_create_from_pixbuf(
            self.pixbuf, 1, None
        )

    def get_useful_height(self):
        aw = self.get_allocated_width()
        pw = self.pixbuf.get_width()
        ph = self.pixbuf.get_height()
        return aw/pw * ph

    def get_scale_factor(self):
        return self.get_allocated_width() / self.pixbuf.get_width()

    def do_draw(self, context):
        sf = self.get_scale_factor()
        context.scale(sf, sf)
        context.set_source_surface(self.img_surface, 0, 0)
        context.paint()
        height = self.get_useful_height()
        self.set_size_request(-1, height)

    def test(self):
        dw = self.get_allocated_width()
        dh = self.get_allocated_height()