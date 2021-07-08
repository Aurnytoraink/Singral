# request.py
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

import requests

class Requests():
    def __init__(self,id,key):
        self.key = key
        self.request = requests.Session()
        self.request.headers.update({
			'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
			"X-App-Id": id})
        self.debug = False

    def update_session(self,method,data):
        self.request.headers.update({method:data})

    def get(self,url,method='get',params=None):
        if self.debug:
            print(url,method,params)
        try:
            if method == 'get':
                return self.request.get(url,params=params)
            else: #POST method
                return self.request.post(url,data=params)
        except:
            print("Request failed!")
            return False

    def set_debug(self,state=bool):
        self.debug = state
