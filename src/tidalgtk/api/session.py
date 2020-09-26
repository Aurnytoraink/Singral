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
import requests
import json
# import tidalgtk.api.spoofbuz as spoofbuz
# import tidalgtk.api.request as request

# FOR DEBUGING ONLY
import request
import spoofbuz
import os
from dotenv import load_dotenv

class Session():
    def __init__(self):
        self.spoofer = spoofbuz.Spoofer()
        self.id = self.spoofer.getAppId()
        self.request = requests.Session()
        self.request.headers.update({
			'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0',
			"X-App-Id": self.id})
        self.base_url = "https://www.qobuz.com/api.json/0.2/"

    def login(self,email=None,pwd=None,token=None):
        if token == None:
            params={
                    "email": email,
                    "password": pwd,
            }
        else:
            params={
                "user_auth_token":token,
            }

        r = self.request.post(self.base_url+"user/login",data=params)
        if r.status_code == 401:
            return False
        elif r.status_code == 400:
            return False
        self.uat = r.json()["user_auth_token"]
        zone = r.json()["user"]["zone"]
        store = r.json()["user"]["store"]
        self.store_token()

        self.request.headers.update({
            "X-User-Auth-Token": self.uat,
            "X-Store": store,
            "X-Zone": zone,})

    def search(self,query,limit=10):
        url = self.base_url + "catalog/search"
        params={
            "query": query,
            "limit": limit
        }
        r = self.request.get(url,params=params)
        results = r.json()
        albums = results["albums"]["items"]
        tracks = results["tracks"]["items"]
        artists = results["artists"]["items"]
        playlists = results["playlists"]["items"]
        return albums, tracks, artists, playlists

# FOR DEBUGING ONLY
load_dotenv()
token = os.getenv('token')
session = Session()
session.login(token=token)
query = str(input("query: "))
result = session.search(query,1)
for i in result:
    print(i,"\n")
