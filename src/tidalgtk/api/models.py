class Album():
    def __init__(self,item):
        self.id = item["id"]
        self.title = item["title"]
        self.duration = item["duration"]
        self.cover = item["image"]["large"]
        if "artist" in item:
            self.artist = Artist(item["artist"])
        self.artistname = item["artist"]["name"]
        self.hires = item["hires"]
        self.date = item["release_date_original"]
        self.explicit = item["parental_warning"]
        if "tracks" in item:
            self.tracks = list(map(lambda x: Track("",x).parse(),item["tracks"]["items"]))

class Track():
    def __init__(self,item):
        self.id = item["id"]
        self.title = item["title"]
        self.duration = item["duration"]
        self.album = Album(item["album"])
        self.cover = self.album.cover
        self.artist = self.album.artist
        if "composer" in item["album"]:
            self.composer = Artist(item["album"]["composer"])
        self.hires = item["hires"]
        self.isrc = item["isrc"]
        self.replaygain_gain = item["audio_info"]["replaygain_track_gain"]
        self.replaygain_peak = item["audio_info"]["replaygain_track_peak"]


class Artist():
    def __init__(self, item):
        self.id = item["id"]
        if item["image"] is None:
            self.cover = None
        elif "mega" in item["image"]:
            self.cover = item["image"]["mega"]
        elif "extralarge" in item["image"]:
            self.cover = item["image"]["extralarge"]
        elif "large" in item["image"]:
            self.cover = item["image"]["large"]
        self.name = item["name"]

class Playlist():
    def __init__(self, item):
        self.id = item["id"]
        if "tracks" in item:
            self.tracks = list(map(lambda x: Track("",x).parse(),item["tracks"]["items"]))
        if "image_rectangle" in item:
            self.cover = item["image_rectangle"][0] #Qobuz playlists
        else:
            self.cover = item["images300"] #User playlists