import os

from tidalgtk.api.models import Track

def get_cover_from_album(item,session):
    if type(item) == Track:
        id = item.album.id
    else:
        id = item.id
    if os.path.isfile(f'/var/cache/files/covers/album_{id}.jpg') is False:
        data = session.get_cover_data(item.cover)
        open(f'/var/cache/files/covers/album_{id}.jpg','xb').write(data)
    else:
        data = open(f'/var/cache/files/covers/album_{id}.jpg','rb').read()
    return data