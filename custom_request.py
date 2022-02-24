from utility import *

## A utility class to make request with proxies !!
## Params use_proxy_param== True ,if want to use proxy for making request else False
## Params use_session== True ,if want to use HTMLSession for making request else False
#                       learn more about requests-html here     -  https://pypi.org/project/requests-html/
class Custom_Requests:
    use_proxy = None
    proxy_handler = None
    def __init__(self,use_proxy_param=False,use_session=True):
        if use_proxy_param:
            proxy_handler = PROXYHANDLER()
            self.proxy_handler = proxy_handler
        if use_session:
            self.session = HTMLSession()
        else:
            self.session = requests
            
    def get(self,url,parser="html.parser",request_type='get',headers=None
                     ,payload=None,params=None,try_times=20):
        retry_times = 0
        response = None
        while retry_times<=try_times:
            try:
                if self.proxy_handler:
                    proxy_option = self.proxy_handler.make_proxy()
                else:
                    proxy_option = None
                if request_type=='get':
                    response = self.session.get(url,proxies=proxy_option,headers=headers,
                                                data=payload,params=params)
                else:
                    response = self.session.post(url,proxies=proxy_option,headers=headers,
                                                data=payload,params=params)
                if response.ok:
                    break
            except:
                #traceback.print_exc()
                retry_times = retry_times + 1
        if response:
            if parser == 'json':
                response = response.json()
            elif parser == 'content':
                response = response.content
            elif parser == 'html.parser':
                response = BeautifulSoup(response.content,parser)
            elif parser == 'xml':
                response = BeautifulSoup(response.content,parser)
            else:
                response = response.content
        return response