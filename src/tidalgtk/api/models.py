import time
import hashlib

class Album():
    def __init__(self, item):
        self.id = item["id"]
        self.title = item["title"]
        self.duration = item["duration"]
        self.cover = item["image"]["large"]
        # self.artist = Artist(item["artist"])
        self.artistname = item["artist"]["name"]
        self.hires = item["hires"]
        self.date = item["release_date_original"]
        self.explicit = item["parental_warning"]

class Track():
    def __init__(self,request,item):
        self.request = request
        self.id = item["id"]
        self.title = item["title"]
        self.duration = item["duration"]
        # self.cover = item["album"]["image"]["large"]
        # self.artist = item["album"]["artist"]
        # self.artistname = item["album"]["artist"]["name"]
        self.album = item["album"]
        self.hires = item["hires"]
        self.isrc = item["isrc"]
        self.replaygain_gain = item["audio_info"]["replaygain_track_gain"]
        self.replaygain_peak = item["audio_info"]["replaygain_track_peak"]

    def get_url(self,quality):
        unix = time.time()
        r_sig = f"trackgetFileUrlformat_id{quality}intentstreamtrack_id{self.id}{unix}{self.request.key}"
        r_sig_hashed = hashlib.md5(r_sig.encode('utf-8')).hexdigest()
        params={
            "request_ts": unix,
            "request_sig": r_sig_hashed,
            "track_id": self.id,
            "format_id": quality,
            "intent": 'stream'}

        return self.request.get("track/getFileUrl?",params=params)


class Artist():
    def __init__(self, item):
        self.id = item["id"]

class Playlist():
    def __init__(self, item):
        self.id = item["id"]