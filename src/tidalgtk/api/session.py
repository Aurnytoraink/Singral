# session.py
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

# import gi
# gi.require_version('Secret', '1')
from gi.repository import GLib
import json
import time
import hashlib
import tidalgtk.api.spoofbuz as spoofbuz
from tidalgtk.api.request import Requests
from tidalgtk.api.models import *
from tidalgtk.api.exceptions import *

# FOR DEBUGING ONLY
# from request import Requests
# import spoofbuz
# from models import *
# from exceptions import *
# import os
# from dotenv import load_dotenv

class Session():
    def __init__(self, app):
        self.app = app
        self.spoofer = spoofbuz.Spoofer() # TODO: Fix issue #4
        self.id = self.spoofer.getAppId()
        self.request = Requests(self.id,"") #Key is set later

    def login(self,email=None,pwd=None,token=None):
        params={
                "email": email,
                "password": pwd,
                "user_auth_token":token,
        }

        r = self.request.get("user/login",'post',params=params)
        if r.status_code == 401:
            GLib.idle_add(function=self.app.on_login_unsucess())
            return
        elif r.status_code == 400:
            GLib.idle_add(function=self.app.on_login_error())
            return
        result = r.json()
        self.uat = result["user_auth_token"]
        self.offer = result["user"]["subscription"]["offer"]
        if self.offer ==  "studio": # Set the maximum quality by default depending on the user's offer
            self.quality = 27
        else:
            self.quality = 6

        if result["user"]["firstname"] is None:
            self.username = result["user"]["display_name"]
        elif result["user"]["lastname"] is None:
            self.username = result["user"]["firstname"]
        else:
            self.username = result["user"]["firstname"] + " " + result["user"]["lastname"]


        self.request.update_session("X-User-Auth-Token",self.uat)
        self.request.update_session("X-Store",result["user"]["store"])
        self.request.update_session("X-Zone",result["user"]["zone"])

        for secret in self.spoofer.getSecrets().values():
            if self.test_secret(secret):
                self.request.key = secret
                break
        GLib.idle_add(function=self.app.on_login_sucess())

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
        r = self.request.get('userLibrary/getAlbumsList?',params=params)
        return r.ok

    def search(self,query,limit=10):
        params={
            "query": query,
            "limit": limit
        }
        r = self.request.get("catalog/search",params=params)
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
        r = self.request.get("album/get",params=params)
        return Album(self.request,r.json())

    def get_track(self,id,limit=100,extra=None):
        params={
            "track_id": id,
            "limit": limit,
            "extra": extra
        }
        r = self.request.get("track/get",params=params)
        return Track(self.request,r.json())

    def get_artist(self,id,extra=None):
        params={
            "artist_id": id,
            "extra": extra
        }
        r = self.request.get("artist/get",params=params)
        return Artist(self.request,r.json())
        

# FOR DEBUGING ONLY
# load_dotenv()
# session = Session("")
# session.login(token=os.getenv('token'))
# session.login(os.getenv('email'),os.getenv('pwd'))


# query = str(input("Search: "))
# result = session.search(query,1)
# for i in result:
#     print(i,"\n")

# result = session.get_album("me0u2on4vwh8a")
# print(result.tracks)

""" Get a track URL"""
# track = session.get_track(62776106)
# track = session.get_track(102280007)
# result = track.get_url(27)
# print(f"⏯Playing: {track.title} from {track.artist.name}")
# print(result)

""" Stream a track from a search"""
# query = str(input("Search: "))
# result = session.search(query,1)
# track = session.get_track(result[1][0]["id"])
# print(f"⏯Playing: {track.title} from {track.artist.name}")
# print(track.get_url(27))

# session.logoff()
# # Supposed to break at this point
# query = str(input("Search: "))
# result = session.search(query,1)
# track = session.get_track(result[1][0]["id"])
# print(f"⏯Playing: {track.title} from {track.artist.name}")
# print(track.get_url(27))
