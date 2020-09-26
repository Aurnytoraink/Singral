class Album():
    def __init__(self, item):
        self.id = item["id"]
        self.title = item["title"]
        self.duration = item["duration"]
        self.cover = item["image"]["large"]
        self.artist = item["artist"]
        self.artistname = item["artist"]["name"]
        self.hires = item["hires"]
        self.date = item["release_data_original"]

class Track():
    def __init__(self, item):
        self.id = item["album"]["id"]
        self.title = item["title"]
        self.duration = item["duration"]
        self.cover = item["album"]["image"]["large"]
        self.artist = item["album"]["artist"]
        self.artistname = item["album"]["artist"]["name"]
        self.album = item["album"]
        self.hires = item["hires"]
        self.isrc = item["isrc"]
        self.replaygain_gain = item["audio_info"]["replaygain_track_gain"]
        self.replaygain_peak = item["audio_info"]["replaygain_track_peak"]

class Artist():
    def __init__(self, item):
        self.id = item["id"]

class Playlist():
    def __init__(self, item):
        self.id = item["id"]