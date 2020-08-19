# download.py
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
import os.path
import os

def dl_image(id, type, url):
    if os.path.isfile('/var/cache/files/covers/{0}_{1}.jpg'.format(type,id)) is False:
        cover = requests.get(url).content
        with open('/var/cache/files/covers/{0}_{1}.jpg'.format(type,id),'xb') as file:
            file.write(cover)
