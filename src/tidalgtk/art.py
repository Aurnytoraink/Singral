from gi.repository import Gdk, Gtk, GdkPixbuf, Handy
from tidalgtk.api.download import get_cover
import cairo
import time

PI = 3.141592653589793

class Artwork():
    def __init__(self):
        return

    def album_artwork(self,album,dimension=200):
        img = Gtk.Image.new()
        get_cover(album.id,'album',album.cover_url)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(f'/var/cache/files/covers/album_{album.id}.jpg',dimension,dimension,True)
        img.set_from_pixbuf(pixbuf)
        img.set_visible(True)
        return img

    def playlist_artwork(self,playlist,dimension=200):
        img = Gtk.Image.new()
        get_cover(playlist.id,'playlist',playlist.picture_url)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(f'/var/cache/files/covers/playlist_{playlist.id}.jpg',dimension,dimension,True)
        img.set_from_pixbuf(pixbuf)
        img.set_visible(True)
        return img

    def artist_artwork(self,artist,dimension=200):
        # If the artist doesn't have a picture (for ex: 6338535)
        if artist.cover_url != None:
            get_cover(artist.id,'artist',artist.cover_url)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(f'/var/cache/files/covers/artist_{artist.id}.jpg',dimension,dimension,True)
            pixbuf = self.round_image(pixbuf)
            img = Gtk.Image.new()
            img.set_from_pixbuf(pixbuf)
            img.set_visible(True)
            return img
        else:
            avatar = Handy.Avatar.new(200,artist.name,True)
            avatar.set_visible(True)
            return avatar

    def round_image(self,pixbuf):
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
