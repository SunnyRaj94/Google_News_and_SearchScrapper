from proxy import *
from custom_request import *
class GFeed:
    # help uri article = https://blog.newscatcherapi.com/google-news-rss/
    topics = ['COVID-19','WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SCIENCE', 'SPORTS', 'HEALTH']
    def __init__(self,use_proxy_param=False, use_session=False,logger=None):
        self.session = Custom_Requests(use_proxy_param,use_session)
        self.logger = logger

    def _write_logs(self,message,log_exception=False):
        if log_exception:
            if self.logger != None:
                self.logger.exception(message)
        else:
            if self.logger != None:
                self.logger.info(message)
    
    def get_articles(self,query_url,formatted=True,feature_image=False,source=False):
        soup = self.make_request(query_url,parser="xml")
        articles = soup.find_all("item")
        if formatted:
            articles = [self.format_article(a,feature_image,source) for a in articles]
        return articles
    
    def make_request(self,url,**kwargs):
        request_type = kwargs.get('request_type', "get")
        headers = kwargs.get('headers',None)
        payload = kwargs.get('payload',None)
        params = kwargs.get('params',None)
        try_times = kwargs.get('try_times', 20)
        parser = kwargs.get('parser', "html.parser")

        
        response = self.session.get(url,parser=parser,request_type=request_type,
                                        headers=headers,payload=payload,params=params,
                                        try_times=try_times)
        return response

    def get_feature_image_and_original_article_link(self,article_url):
        response = self.make_request(article_url,parser='no_content')
        original_url = response.url
        soup = BeautifulSoup(response.content,'html.parser')
        feature_image = self.get_feature_image(article_url,soup)
        return original_url,feature_image
    
    def get_feature_image(self,article_url,soup=None):
        try:
            if soup == None:
                soup = self.make_request(article_url,parser='html.parser')
            element = soup.find('meta',property="og:image") if soup.find('meta',property="og:image") else soup.find('meta',itemprop="image")
            return element.get("content") if element else element
        except:
            return None
    
    def format_article(self,article,feature_image=False,source=False):
        data = {}
        data['title'] = article.title.text
        data['link'] = article.link.text
        data['pubDate'] = article.pubDate.text
        data['description'] = article.description.text
        if feature_image:
            data['feature_image'] = self.get_feature_image(article.link.text)
        if source:
            element = article.source
            data['source_name'] = element.get_text() if element else element
            data['source_url'] = element.get("url") if element else element
        return data
    
    def make_query_url(self,lang,query,hours=1,geo=False,country='IN'):
        if geo:
            url =  "https://news.google.com/rss/geo/"+ query.replace(" ","%20") + f"?%20when%3A{hours}h&hl={lang}&gl={country}&ceid={country}:{lang}"
        else:
            url =  "https://news.google.com/rss/search?q="+ query.replace(" ","%20") + f"%20when%3A{hours}h&hl={lang}&gl={country}&ceid={country}:{lang}"
        return url

    def make_topic_url(self,lang,topic=None,hours=3,country='IN'):
        ceid = f"when%3A{hours}h&hl={lang}&gl={country}&ceid={country}:{lang}".replace(":","%3A")
        
        if topic:
            if topic.upper() in self.topics:
                headlines = f'https://news.google.com/rss/headlines/section/topic/{topic.upper()}?' + ceid
                return headlines
            else:
                headlines = f'https://news.google.com/rss/headlines?' + ceid
                return headlines
        else:
            headlines = f'https://news.google.com/rss/headlines?' + ceid
            return headlines

    def lang_articles(self,lang,query,hours=1):
        if query.upper() in self.topics:
            lang_url = self.make_topic_url(lang,query,hours)
        else:
            lang_url = self.make_query_url(lang,query,hours)
        lang_articles = self.get_articles(lang_url)
        self._write_logs(f"articles got for params -- {lang} . {query} , {hours}   is -- {len(lang_articles)}")
        lang_articles = self.find_new_articles(lang_articles)
        self._write_logs(f"new articles for params -- {lang} . {query} , {hours}   is -- {len(lang_articles)}")
        lang_artiles_data = []
        for ar in lang_articles[:50]:
            try:
                self._write_logs("parsing article")
                data = self.format_article(ar)
                if self.formatted:
                    raw_data = self.raw_articles(data,lang,query)
                    lang_artiles_data.append(raw_data)
                else:
                    lang_artiles_data.append(data)
                if len(lang_artiles_data)>=20:
                    break
            except:
                self._write_logs("article skipped",True)

        self._write_logs(f"total articles generated for  params --   lang - {lang}  , query - {query}  , hours -  {hours}    is -- {len(lang_artiles_data)}")
        return lang_artiles_data
    
    def get_section_url(self,lang,topic,section,hours=6):
        lang = lang.lower().strip()
        topic = topic.upper().strip()
        section = section.upper().strip()
        #BASE = 'https://news.google.com/rss/topics/'
        BASE = 'https://news.google.com/topics/'
        ceid = f"?when%3A{hours}h&hl={lang}&gl=IN&ceid=IN:{lang}"
        if lang in LANGS:
            lang_records = TOPICS_DICT[lang]
            if topic in TOPICS:
                topic_records = lang_records[topic]
                if section in topic_records:
                    section_record = [a for a in value_dicts if a['section_mapped']==section and
                                      a['topic_mapped']==topic and a['lang']==lang][0]
                    print(section_record)
                    section_url = BASE+section_record['topic_hash']+'/sections/' +section_record['section_hash']+ceid
                    return section_url
                else:
                    if topic_records == []:
                        raise Exception(f"there is no sub-section available for this language-topic {lang} - {topic}")
                    else:
                        raise Exception(f"sub-section not available for this language-topic {lang} - {topic} must enter one of sections in {','.join(topic_records)}")
            else:
                raise Exception(f"topic is not valid must enter one of topics in {','.join(TOPICS)}")
        else:
            raise Exception(f"language is not valid must enter one of languages in {','.join(LANGS)}")