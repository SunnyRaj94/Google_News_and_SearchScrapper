from proxy import *
from custom_request import *
from joblib import Parallel, delayed

## TIPS TO IMPROVE GOOGLE SEARCH RESULTS 
"""
I. Basic search operators
    " "	"nikola tesla"
    Put any phrase in quotes to force Google to use exact-match. On single words, prevents synonyms.
    OR	tesla OR edison
    Google search defaults to logical AND between terms. Specify "OR" for a logical OR (ALL-CAPS).
    |	tesla | edison
    The pipe (|) operator is identical to "OR". Useful if your Caps-lock is broken :)
    ( )	(tesla OR edison) alternating current
    Use parentheses to group operators and control the order in which they execute.
    -	tesla -motors
    Put minus (-) in front of any term (including operators) to exclude that term from the results.
    *	tesla "rock * roll"
    An asterisk (*) acts as a wild-card and will match on any word.
    #..#	tesla announcement 2015..2017
    Use (..) with numbers on either side to match on any integer in that range of numbers.
    $	tesla deposit $1000
    Search prices with the dollar sign ($). You can combine ($) and (.) for exact prices, like $19.99.
    €	€9,99 lunch deals
    Search prices with the Euro sign (€). Most other currency signs don't seem to be honored by Google. 
    in	250 kph in mph
    Use "in" to convert between two equivalent units. This returns a special, Knowledge Card style result.
    Advanced search operators are special commands that modify searches and may require additional parameters (such as a domain name). Advanced operators are typically used to narrow searches and drill deeper into results.
II. Advanced search operators
    intitle:	intitle:"tesla vs edison"
    Search only in the page's title for a word or phrase. Use exact-match (quotes) for phrases.
    allintitle:	allintitle: tesla vs edison
    Search the page title for every individual term following "allintitle:". Same as multiple intitle:'s.
    inurl:	tesla announcements inurl:2016
    Look for a word or phrase (in quotes) in the document URL. Can combine with other terms.
    allinurl:	allinurl: amazon field-keywords nikon
    Search the URL for every individual term following "allinurl:". Same as multiple inurl:'s.
    intext:	intext:"orbi vs eero vs google wifi"
    Search for a word or phrase (in quotes), but only in the body/document text.
    allintext:	allintext: orbi eero google wifi
    Search the body text for every individual term following "allintext:". Same as multiple intexts:'s.
    filetype:	"tesla announcements" filetype:pdf
    Match only a specific file type. Some examples include PDF, DOC, XLS, PPT, and TXT.
    related:	related:nytimes.com
    Return sites that are related to a target domain. Only works for larger domains.
    AROUND(X)	tesla AROUND(3) edison
    Returns results where the two terms/phrases are within (X) words of each other.
    Unreliable operators have either been found to produce inconsistent results or have been deprecated altogether. The "link:" operator was officially deprecated in early 2017. It appears that "inanchor:" operators are still in use, but return very narrow and sometimes unreliable results. Use link-based operators only for initial research.
III. Unreliable/deprecated operators
        ~	~cars
        Include synonyms. Seems to be unreliable, and synonym inclusion is default now.
        +	+cars
        Force exact-match on a single phrase. Deprecated with the launch of Google+.
        daterange:	tesla announcements daterange:2457663-2457754
        Return results in the specified range. Can be inconsistent. Requires Julian dates.
        link:	link:nytimes.com
        Find pages that link to the target domain. This operator was deprecated in early 2017.
        inanchor:	inanchor:"tesla announcements"
        Find pages linked to with the specified anchor text/phrase. Data is heavily sampled.
        allinanchor:	allinanchor: tesla announcements
        Find pages with all individual terms after "inanchor:" in the inbound anchor text.
        Note that, for all of the "allin...:" operators, Google will try to apply the operator to every term following it. Combining "allin...:" operators with any other operators will almost never produce the desired results.
    1. Chain together operator combos
    You can chain together almost any combination of text searches, basic operators, and advanced operators:
    "nikola tesla" intitle:"top 5..10 facts" -site:youtube.com inurl:2015
    This search returns any pages that mention "Nikola Tesla" (exact-match), have the phrase "Top (X) facts" in the title, where X ranges from 5 to 10, are not on YouTube.com, and have "2015" somewhere in the URL.
    2. Hunt down plagiarized content
    Trying to find out if your content is unique or if someone is plagiarizing you? Use a unique phrase from your text, put it in quotes (exact-match) after an "intext:" operator, and exclude your own site with "-site:"...
    intext:"they were frolicking in our entrails" -site:moz.com
    Similarly, you can use "intitle:" with a long, exact-match phrase to find duplicate copies of your content.
    3. Audit your HTTP->HTTPS transition
    Switching a site from HTTP to HTTPS can be challenging. Double-check your progress by seeing how many of each type of page Google has indexed. Use the "site:" operator on your root domain and then exclude HTTPS pages with "-inurl:"...
    site:moz.com -inurl:https
    This will help you track down any stragglers or find pages that might not have been re-crawled by Google.
    These are just a few examples of a nearly infinite set of combinations. Looking for more examples? You're in luck! We've created a mega-list of 67 examples to catapult you toward site operator mastery.
"""
#### SITES FOR REFFERENCE ? HELP
"""
https://moz.com/learn/seo/search-operators
https://www.lifehack.org/articles/technology/20-tips-use-google-search-efficiently.html
"""




class GSearch:
    use_proxy = None
    
    search_types = {'applications': 'app', 'blogs': 'blg', 'books': 'bks',
                  'discussions': 'dsc', 'images': 'isch', 'news': 'nws',
                  'patents': 'pts', 'places': 'plcs', 'recipes': 'rcp',
                  'shopping': 'shop', 'video': 'vid'}
    
    advance_search_operators = ['intitle', 'allintitle', 'inurl', 'allinurl', 'intext', 'allintext', 'filetype', 'related','site']
    
    BASE_URL = "https://www.google.com/search?q="
    
    search_query,search_type,page_count,proxy_handler = None , None,None,None
    
    search_results = []
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
    
    def __make_request(self,url,parser="html.parser"):
        response = self.session.get(url,parser=parser,request_type='get',
                                        headers=None,payload=None,params=None,
                                        try_times=20)
        return response
    
    def __parse_soup__(self,query_url):
        response = self.__make_request(query_url)
        result = []
        for g in response.find_all(class_='g'):
            try:
                data = {"title":g.find("h3").text,"description":g.text}
                data['links'] = [a['href'] for a in g.find_all("a") if "href" in a.attrs]
                result.append(data)
            except:
                pass
        self.search_results = self.search_results + result
        
    def get_images_from_page(self,soup):
        scripts = [a for a in soup.select("script") if "AF_initDataCallback" in str(a)]
        script_string = get_needed_string(scripts[-1].string,'AF_initDataCallback(',");")
        json_data = json.loads(get_needed_string(script_string,'hash: \'2\', data:',', sideChannel: {}}'))
        images = list(set([a for a in extract_strings(json_data) if isinstance(a,str)
                                                                     and a.startswith("https://encrypted-tbn0.gstatic.com")]))
        return images
    
    def _generate_urls_(self,query,search_type=None,page_count=20,**kwargs):
        advance_search_operators_from_param = {}
        if search_type:
            if search_type not in self.search_types.keys():
                raise ValueError(f"search_type takes one in the following arguments  -:- {list(self.search_types.keys())}")
        search_query = query.replace(" ","+")
        for k,v in kwargs.items():
            if k in self.advance_search_operators:
                advance_search_operators_from_param[k]=v
            else:
                raise ValueError(f"advance_search_operators takes following arguments  -:- {self.advance_search_operators}")
        
        query_urls = []
        for page in range(page_count):
            __query__ = ""
            for k,v in advance_search_operators_from_param.items():
                __query__ = __query__ + f"{k}%3A" + v + "+"
            __query__ = __query__ + search_query
            if search_type:
                __query__ = __query__ +"&tbm="+self.search_types[search_type]
            __query__ = __query__ +'&start=' + str((int(page)*10))
            query_urls.append(self.BASE_URL+__query__)
        return query_urls
    
    def get_results(self,query_urls,parallel_threads=5,use_parallel=False):
        if use_parallel:
            res = Parallel(n_jobs=parallel_threads, require='sharedmem')(delayed(self.__parse_soup__)(url) for url in tqdm(query_urls))
        else:
            for url in query_urls:
                #time.sleep(random.randint(1,5))
                self.__parse_soup__(url)
        response = self.search_results[:]
        self.search_results = []
        return response
    
    def get_images_from_search(self,soup):
        all_script_tags = soup.select('script')
        matched_images_data = ''.join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))
        matched_images_data_fix = json.dumps(matched_images_data)
        matched_images_data_json = json.loads(matched_images_data_fix)

        # matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]",
        #                                                     matched_images_data_json)
        matched_google_image_data = re.findall(r'\[\"GRID_STATE0\",null,\[\[1,\[0,\".*?\",(.*),\"All\",', matched_images_data_json)
        matched_google_images_thumbnails = ', '.join(
                re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                        str(matched_google_image_data))).split(', ')
        images = []
        for fixed_google_image_thumbnail in matched_google_images_thumbnails:
            # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
            google_image_thumbnail_not_fixed = bytes(fixed_google_image_thumbnail, 'ascii').decode('unicode-escape')

            # after first decoding, Unicode characters are still present. After the second iteration, they were decoded.
            google_image_thumbnail = bytes(google_image_thumbnail_not_fixed, 'ascii').decode('unicode-escape')
            images.append(google_image_thumbnail)
        return images