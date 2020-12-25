import requests

class Requests():
    def __init__(self,id,key):
        self.key = key
        self.base_url = "https://www.qobuz.com/api.json/0.2/"
        self.request = requests.Session()
        self.request.headers.update({
			'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0',
			"X-App-Id": id})
        self.debug = False

    def update_session(self,method,data):
        self.request.headers.update({method:data})

    def get(self,url,method='get',params=None):
        if self.debug:
            print(url,method,params)
        try:
            if method == 'get':
                return self.request.get(self.base_url+url,params=params)
            else: #POST method
                return self.request.post(self.base_url+url,data=params)
        except:
            print("Request failed!")
            return False

    def set_debug(self,state=bool):
        self.debug = state