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
        return soup
    
    def get_articles(self,query_url,formatted=True):
        # soup = BeautifulSoup(requests.get(query_url).content,"xml")
        soup = self.session.get(query_url,parser="xml",request_type='get',
                                        headers=None,payload=None,params=None,
                                        try_times=20)
        articles = soup.find_all("item")
        if formatted:
            articles = [self.format_article(a) for a in articles]
        return articles

    def get_feature_image(self,article_url):
        # soup = BeautifulSoup(requests.get(article_url).content,"html.parser")
        soup = self._soup(article_url)
        return soup.find('meta',property="og:image")['content']

    def format_article(self,article,feature_image=False):
        data = {}
        data['title'] = article.title.text
        data['link'] = article.link.text
        data['pubDate'] = article.pubDate.text
        data['description'] = article.description.text
        if feature_image:
            data['feature_image'] = self.get_feature_image(article.link.text)
        return data
    
    def make_query_url(self,lang,query,hours=1):
        url =  "https://news.google.com/rss/search?q="+ query.replace(" ","%20") + f"%20when%3A{hours}h&hl={lang}&gl=IN&ceid=IN:{lang}"
        return url

    def make_topic_url(self,lang,topic,hours=3):
        ceid = f"when%3A{hours}h&hl={lang}&gl=IN&ceid=IN:{lang}".replace(":","%3A")
        
        if topic.upper() in self.topics:
            headlines = f'https://news.google.com/rss/headlines/section/topic/{topic.upper()}?' + ceid
            return headlines
        else:
            return "invalid topic"

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