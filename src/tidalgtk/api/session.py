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
# from gi.repository import Secret
import json
import time
import hashlib
# import tidalgtk.api.spoofbuz as spoofbuz
# import tidalgtk.api.request as request
# from tidalgtk.api.models import *
# from tidalgtk.api.exceptions import *

# FOR DEBUGING ONLY
from request import Requests
import spoofbuz
from models import *
from exceptions import *
import os
from dotenv import load_dotenv

class Session():
    def __init__(self):
        self.spoofer = spoofbuz.Spoofer()
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
            raise InvalidCreditentials("Invalid username/email and password combination")
        elif r.status_code == 400:
            raise InternalError("An error occured")
        self.uat = r.json()["user_auth_token"]

        self.request.update_session("X-User-Auth-Token",self.uat)
        self.request.update_session("X-Store",r.json()["user"]["store"])
        self.request.update_session("X-Zone",r.json()["user"]["zone"])

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
        return Album(r.json())

    def get_track(self,id,limit=100,extra=None):
        params={
            "track_id": id,
            "limit": limit,
            "extra": extra
        }
        r = self.request.get("track/get",params=params)
        return Track(self.request,r.json())

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
        print(r.content)
        return r.ok

    def setup_secret(self):
        for secret in self.spoofer.getSecrets().values():
            if self.test_secret(secret):
                self.request.key = secret
                print(secret)
                break

# FOR DEBUGING ONLY
load_dotenv()
token = os.getenv('token')
email = os.getenv('email')
pwd = os.getenv('pwd')

session = Session()
session.login(token=token)
# session.login(email,pwd)
session.setup_secret()


# query = str(input("Search: "))
# result = session.search(query,1)
# for i in result:
#     print(i,"\n")

# result = session.get_album("z395ggwwn3qka")
# print(result)

track = session.get_track(72956512)
result = track.get_url(27)
print(result)
print(result.json())