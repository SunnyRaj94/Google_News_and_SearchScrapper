from utility import *
class PROXYHANDLER():
    proxy_cycle = None
    proxies_list = []
    proxy_used = 0
    IP = None
    
    def __init__(self,recall_proxy_interval = 5):
        self.recall_proxy_interval = recall_proxy_interval
        self._call_forproxies()


    def _check_to_call_proxy(self):
        if self.proxy_used % self.recall_proxy_interval == 0:
            self._call_forproxies()


    def _call_forproxies(self):
        try_times = 10
        while try_times != 0:
            try:
                self.obtain_free_Proxy_list()
                self.shuffel_proxies()
                break
            except:
                time.sleep(3)
                try_times = try_times - 1

    def obtain_free_Proxy_list(self):
        session = HTMLSession()
        soup = BeautifulSoup(session.get('https://www.sslproxies.org').content,"html.parser")
        final_proxies = []
        for a in soup.find("table").find_all("tr"):
            if "sec" in a.text:
                final_proxies.append(a.find("td").text)
        self.proxies_list = final_proxies
    
    def shuffel_proxies(self):
        random.shuffle(self.proxies_list)
        self.proxy_cycle = cycle(self.proxies_list)


    def make_proxy(self):
        PROXY = next(self.proxy_cycle)
        self.proxy_used = self.proxy_used + 1
        self._check_to_call_proxy()
        return {'http': "http://" + PROXY,}

   
    def get_ip(self):
        api_url = 'https://api.ipify.org?format=json'
        return requests.get(api_url).json()['ip']

    def get_ip_address_by_google(self):
        sess = HTMLSession()
        rrr = "https://www.google.com/search?ei=uihSYKirGpPB3LUP_Li3gAk&q=what+is+my+ip"
        res = sess.get(rrr).content
        res = BeautifulSoup(res,"lxml")
        res = res.find("span",style="font-size:20px").text
        return res