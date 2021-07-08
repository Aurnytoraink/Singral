# qobuz.py
#
# Copyright 2021 Aurnytoraink
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

import time
import hashlib
# import singral.api.spoofbuz as spoofbuz
# from singral.api.request import Requests
# from singral.api.models import Album, Artist, Track, Playlist

# FOR DEBUGING ONLY
# from request import Requests
# import spoofbuz
# from models import Album, Artist, Track, Playlist, UserSession
# import json

class Qobuz():
    def __init__(self):
        self.base_url = "https://www.qobuz.com/api.json/0.2/"
        self.spoofer = spoofbuz.Spoofer()
        self.id = self.spoofer.getAppId()
        self.request = Requests(self.id,"") #Key is set later

    def login(self,email=None,pwd=None,token=None):
        params={
                "email": email,
                "password": pwd,
                "user_auth_token":token,
        }

        r = self.request.get(self.base_url+"user/login",'post',params=params)
        if r.status_code == 401:
            return False, True
        elif r.status_code == 400:
            return False, False
        result = r.json()

        self.session = UserSession(result)

        self.username = result["user"]["display_name"]
        self.user_id = result["user"]["id"]
        self.uat = result["user_auth_token"]
        self.offer = result["user"]["subscription"]["offer"]
        # Set the maximum quality by default depending on the user's offer
        if self.offer ==  "studio":
            self.quality = 27
        else:
            self.quality = 6


        self.request.update_session("X-User-Auth-Token",self.uat)
        self.request.update_session("X-Store",result["user"]["store"])
        self.request.update_session("X-Zone",result["user"]["zone"])

        for secret in self.spoofer.getSecrets().values():
            if self.test_secret(secret):
                self.request.key = secret
                break
        return True

    def logoff(self):
        """ Log off:
            This overwrite the old request session by a new one """
        self.uat =  ""
        self.request = Requests(self.id,"")

    def test_secret(self,key):
        unix = time.time()
        r_sig = "userLibrarygetAlbumsList" + str(unix) + key
        r_sig_hashed = hashlib.md5(r_sig.encode('utf-8')).hexdigest()
        params={
            "app_id": self.id,
            "user_auth_token": self.uat,
            "request_ts": unix,
            "request_sig": r_sig_hashed}
        r = self.request.get(self.base_url+'userLibrary/getAlbumsList?',params=params)
        return r.ok

########## ACTIONS ##########

    def search(self,query,limit=10):
        params={
            "query": query,
            "limit": limit
        }
        r = self.request.get(self.base_url+"catalog/search",params=params)
        results = r.json()
        albums = results["albums"]["items"]
        tracks = results["tracks"]["items"]
        artists = results["artists"]["items"]
        playlists = results["playlists"]["items"]
        return albums, tracks, artists, playlists

    def get_album(self,id,limit=100,extra=None):
        params={
            "album_id": id,
            "limit": limit,
            "extra": extra
        }
        r = self.request.get(self.base_url+"album/get",params=params)
        return Album(r.json())

    def get_track(self,id,limit=100,extra=None):
        params={
            "track_id": id,
            "limit": limit,
            "extra": extra
        }
        r = self.request.get(self.base_url+"track/get",params=params)
        return Track(r.json())

    def get_artist(self,id,extra=None):
        params={
            "artist_id": id,
            "extra": extra
        }
        r = self.request.get(self.base_url+"artist/get",params=params)
        return Artist(r.json())

########## USERFAV ##########

    def get_userfav_albums(self,limit=50,offset=0):
        params = {
            "limit" : limit,
            "offset" : offset,
            "type" : "albums",
            "user_id": self.user_id
        }
        r = self.request.get(self.base_url+"favorite/getUserFavorites",params=params)
        return list(map(lambda x: Album(x),r.json()["albums"]["items"]))

    def get_userfav_artists(self,limit=50,offset=0):
        params = {
            "limit" : limit,
            "offset" : offset,
            "type" : "artists",
            "user_id": self.user_id
        }
        r = self.request.get(self.base_url+"favorite/getUserFavorites",params=params)
        return list(map(lambda x: Artist(x),r.json()["artists"]["items"]))

    def get_userfav_tracks(self,limit=50,offset=0):
        params = {
            "limit" : limit,
            "offset" : offset,
            "type" : "tracks",
            "user_id": self.user_id
        }
        r = self.request.get(self.base_url+"favorite/getUserFavorites",params=params)
        return list(map(lambda x: Track(x),r.json()["tracks"]["items"]))

    def get_userfav_playlists(self,limit=50,offset=0):
        params = {
            "limit" : limit,
            "offset" : offset,
            "user_id": self.user_id
        }
        r = self.request.get(self.base_url+"playlist/getUserPlaylists",params=params)
        return list(map(lambda x: Playlist(x),r.json()["playlists"]["items"]))

    def get_streamable_url(self,track):
        unix = time.time()
        r_sig = f"trackgetFileUrlformat_id{self.quality}intentstreamtrack_id{track.id}{unix}{self.request.key}"
        r_sig_hashed = hashlib.md5(r_sig.encode('utf-8')).hexdigest()
        params={
            "request_ts": unix,
            "request_sig": r_sig_hashed,
            "track_id": track.id,
            "format_id": self.quality,
            "intent": 'stream'}

        return self.request.get(self.base_url+"track/getFileUrl?",params=params).json()["url"]

    def get_cover_data(self,url):
        return self.request.get(url).content



# FOR DEBUGING ONLY
# from pathlib import Path
# PATH = Path("/home/aurnytoraink/Projets/Applications/Singral/src/api/")

# session = Qobuz()

# mail = json.loads(open(PATH/"config.json",'rb').read())["email"]
# pwd = json.loads(open(PATH/"config.json",'rb').read())["pwd"]
# session.login(mail,pwd)

# token = json.loads(open(PATH/"config.json",'rb').read())["uat"]
# session.login(token=token)

# print("Logged!")
# print(f"Welcome {session.username}")


# query = str(input("Search: "))
# result = session.search(query,1)
# for i in result:
#     print(i,"\n")

# result = session.get_album("me0u2on4vwh8a")
# print(result.tracks)

# """ Get a track URL"""
# track = session.get_track(62776106)
# track = session.get_track(102280007)
# result = session.get_streamable_url(track)
# print(f"⏯Playing: {track.title} from {track.artist.name}")
# print(result)

# """ Stream a track from a search"""
# query = str(input("Search: "))
# result = session.search(query,1)
# track = session.get_track(result[1][0]["id"])
# print(f"⏯Playing: {track.title} from {track.artist.name}")
# print(session.get_streamable_url(track))

# session.logoff()
# # Supposed to break at this point
# query = str(input("Search: "))
# result = session.search(query,1)
# track = session.get_track(result[1][0]["id"])
# print(f"⏯Playing: {track.title} from {track.artist.name}")
# print(session.get_streamable_url(track))

# from random import choice

# start = time.time()
# tracks = session.get_userfav_tracks(50,50)
# end = time.time()
# track = choice(tracks)
# print(end-start)
# print(session.get_streamable_url(track))
