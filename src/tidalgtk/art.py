from gi.repository import Gdk
import cairo
import time

PI = 3.141592653589793

def round_image(pixbuf):
    size = pixbuf.get_width()
    surface = cairo.ImageSurface(cairo.Format.ARGB32, size, size)
    ctx = cairo.Context(surface)
    ctx.arc(size/2, size/2, size/2, 0, 2 * PI)
    ctx.clip()
    ctx.new_path()
    Gdk.cairo_set_source_pixbuf(ctx,pixbuf,0,0)
    ctx.paint()
    dest = Gdk.pixbuf_get_from_surface(surface, 0, 0, size, size);
    end = time.time()
    return dest
