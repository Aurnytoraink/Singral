from gi.repository import Gtk, Handy, Gdk, GdkPixbuf, GLib, Pango
from tidalgtk.api.download import get_cover
import cairo
import time

PI = 3.141592653589793

class Artwork():
    def __init__(self):
        return

    def album_pixbuf(self,album,dimension=175):
        get_cover(album.id,'album',album.cover)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(f'/var/cache/files/covers/album_{album.id}.jpg',dimension,dimension,True)
        return pixbuf

    def album_artwork(self,album,dimension=175):
        img = Gtk.Image.new()
        get_cover(album.id,'album',album.cover)
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

    def artist_artwork(self,artist,dimension=150):
        # If the artist doesn't have a picture
        if artist.cover != None:
            get_cover(artist.id,'artist',artist.cover)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(f'/var/cache/files/covers/artist_{artist.id}.jpg',dimension,dimension,True)
            avatar = Handy.Avatar.new(dimension,"",True)
            avatar.set_image_load_func(Handy.AvatarImageLoadFunc(pixbuf))
            data = Handy.AvatarImageLoadFunc(dimension,pixbuf)
            img = Gtk.Image.new()
            img.set_from_pixbuf(pixbuf)
            img.set_visible(True)
            return img
        else:
            avatar = Handy.Avatar.new(dimension,artist.name,True)
            avatar.set_visible(True)
            return avatar

    def album_boxchild(self,album):
        img = self.album_artwork(album)
        name = Gtk.Label.new()
        name.set_markup(
            "<b>" + GLib.markup_escape_text(album.title) + "</b>")
        name.set_ellipsize(Pango.EllipsizeMode(3))
        name.set_max_width_chars(0)
        artistname = Gtk.Label.new(album.artist.name)
        artistname.set_ellipsize(Pango.EllipsizeMode(3))
        box = Gtk.Box.new(Gtk.Orientation(1),0)
        box.pack_start(img,False,False,0)
        box.pack_start(name,False,False,0)
        box.pack_start(artistname,False,False,0)
        box.set_halign(Gtk.Align.CENTER)
        box.set_valign(Gtk.Align.CENTER)
        box.set_visible(True)
        name.set_visible(True)
        artistname.set_visible(True)
        return box

    def artist_boxchild(self,artist):
        img = self.artist_artwork(artist)
        name = Gtk.Label.new()
        name.set_markup(
            "<b>" + GLib.markup_escape_text(artist.name) + "</b>")
        name.set_ellipsize(Pango.EllipsizeMode(3))
        name.set_max_width_chars(0)
        box = Gtk.Box.new(Gtk.Orientation(1),0)
        box.pack_start(img,False,False,0)
        box.pack_start(name,False,False,0)
        box.set_halign(Gtk.Align.CENTER)
        box.set_valign(Gtk.Align.CENTER)
        box.set_visible(True)
        name.set_visible(True)
        return box

    def playlist_boxchild(self,playlist):
        img = self.playlist_artwork(playlist)
        name = Gtk.Label.new()
        name.set_markup(
            "<b>" + GLib.markup_escape_text(playlist.name) + "</b>")
        name.set_ellipsize(Pango.EllipsizeMode(3))
        box = Gtk.Box.new(Gtk.Orientation(1),0)
        box.pack_start(img,False,False,0)
        box.pack_start(name,False,False,0)
        box.set_visible(True)
        name.set_visible(True)
        return box

    def track_boxchild(self,track):
        img = self.album_artwork(track.album,50)
        name = Gtk.Label.new()
        name.set_markup(
            "<b>" + GLib.markup_escape_text(track.title) + "</b>")
        name.set_ellipsize(Pango.EllipsizeMode(3))
        name.set_xalign(0)
        artist = Gtk.Label.new(track.artist.name)
        artist.set_ellipsize(Pango.EllipsizeMode(3))
        artist.set_xalign(0)
        box_name = Gtk.Box.new(Gtk.Orientation(1),0)
        box_name.pack_start(name,False,False,0)
        box_name.pack_start(artist,False,False,0)
        box = Gtk.Box.new(Gtk.Orientation(0),0)
        box.pack_start(img,False,False,0)
        box.pack_start(box_name,False,False,0)
        box.set_visible(True)
        box.set_spacing(10)
        name.set_visible(True)
        artist.set_visible(True)
        box_name.set_visible(True)
        return box

    def round_image(self,pixbuf):
        size = pixbuf.get_height()
        surface = cairo.ImageSurface(cairo.Format.ARGB32, size, size)
        ctx = cairo.Context(surface)
        ctx.arc(size/2, size/2, size/2, 0, 2 * PI)
        ctx.clip()
        ctx.new_path()
        Gdk.cairo_set_source_pixbuf(ctx,pixbuf,0,0)
        ctx.paint()
        dest = Gdk.pixbuf_get_from_surface(surface, 0, 0, size, size);
        return dest
