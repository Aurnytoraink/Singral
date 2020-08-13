class Track():
	def __init__(self, uri, title, artist, duration, cover, like=False):
		self.uri = uri
		self.title = title
		self.artist = artist
		self.duration = duration
		self.cover = cover
		self.like = like
