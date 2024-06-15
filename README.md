## Google_News_and_SearchScrapper
**is a powerful Python tool designed to programmatically extract and parse results from Google Search and Google News.\
Whether you're conducting research, gathering competitive intelligence, or monitoring news developments,\
this repository provides a streamlined way to access Google’s vast repository of information.**

## Features
- Comprehensive Results Parsing: Effortlessly retrieve all found links, titles, and descriptions from Google Search and Google News.
- Structured Output: Outputs results in a clean Python dictionary format for easy integration with other applications and workflows.
- Proxy Support: Enhance your scraping process with built-in support for proxies to manage requests and avoid potential rate limiting by Google.

## Use Cases
- Research: Quickly gather data from Google searches and news articles for academic, market, or competitive research.
- News Monitoring: Keep track of the latest news across various topics and regions.
- Data Aggregation: Collect and compile data from Google's search results for analysis or reporting.

## Installation
To install the Google_News_and_SearchScrapper, clone this repository and install the necessary dependencies:
```
  git clone https://github.com/yourusername/Google_News_and_SearchScrapper.git
  cd Google_News_and_SearchScrapper
  pip install -r requirements.txt

```
## Usage
***Below is a simple example of how to use the scraper:***


## Scrape news articles from google news

## Proxy Configuration
To use proxies with the scrapper, simply pass a list of proxy URLs when initializing the scrapper.
```
PARAMS ---
use_proxy_param --- It enables to use proxy for scrapping

use_session     --- It uses request-html instead of requests

logger          --- if you want to log // you can pass your logger

you can scrape articles from any of these topics -- 

COVID-19,WORLD,NATION,BUSINESS,TECHNOLOGY,ENTERTAINMENT,SCIENCE,SPORTS,HEALTH

you can scrape articles from any of these languages -- 

ta,gu,en,bn,kn,mr,te,ml,hi
```
------------------------------------------------------------------------------------------------------------------------------------------------------------
```
from GoogleRssFeed import *

gfeed = GFeed()

lang,topic,hours='hi','BUSINESS',10

topic_url = gfeed.make_topic_url(lang,topic,hours)

##### topic url looks like 
https://news.google.com/rss/headlines/section/topic/BUSINESS?when%3A10h&hl=hi&gl=IN&ceid=IN%3Ahi

articles = gfeed.get_articles(topic_url)

##### articles have these keys 
dict_keys(['title', 'link', 'pubDate', 'description'])

##### articles response looks like 


{'title': 'Taking Stock: यूक्रेन पर रूस की नरमी से बाजार में रौनक, निफ्टी में दिखी 509 अंकों की इंट्रा-डे तेजी, - मनी कंट्रोल',
 'link': 'https://news.google.com/__i/rss/rd/articles/CBMixgFodHRwczovL2hpbmRpLm1vbmV5Y29udHJvbC5jb20vbmV3cy9tYXJrZXRzL3Rha2luZy1zdG9jay1ydXNzaWFzLXNvZnRuZXNzLW9uLXVrcmFpbmUtYnJpZ2h0ZW5zLXRoZS1tYXJrZXQtbmlmdHktc2Vlcy1hbi1pbnRyYS1kYXktcmlzZS1vZi01MDktcG9pbnRzLWtub3ctaG93LXRoZS1tYXJrZXQtbWF5LW1vdmUtdG9tb3Jyb3ctNDQ4NTMxLmh0bWzSAQA?oc=5',
 'pubDate': 'Tue, 15 Feb 2022 11:41:00 GMT',
 'description': '<ol><li><a href="https://news.google.com/__i/rss/rd/articles/CBMixgFodHRwczovL2hpbmRpLm1vbmV5Y29udHJvbC5jb20vbmV3cy9tYXJrZXRzL3Rha2luZy1zdG9jay1ydXNzaWFzLXNvZnRuZXNzLW9uLXVrcmFpbmUtYnJpZ2h0ZW5zLXRoZS1tYXJrZXQtbmlmdHktc2Vlcy1hbi1pbnRyYS1kYXktcmlzZS1vZi01MDktcG9pbnRzLWtub3ctaG93LXRoZS1tYXJrZXQtbWF5LW1vdmUtdG9tb3Jyb3ctNDQ4NTMxLmh0bWzSAQA?oc=5" target="_blank">Taking Stock: यूक्रेन पर रूस की नरमी से बाजार में रौनक, निफ्टी में दिखी 509 अंकों की इंट्रा-डे तेजी,</a>&nbsp;&nbsp;<font color="#6f6f6f">मनी कंट्रोल</font></li><li><a href="https://news.google.com/__i/rss/rd/articles/CBMipgFodHRwczovL3d3dy56ZWViaXouY29tL2hpbmRpL3N0b2NrLW1hcmtldHMvbGl2ZS11cGRhdGVzLXN0b2NrLW1hcmtldC1saXZlLW9uLTE1LWZlYnJ1YXJ5LWRvdy1qb25lcy1zZ3gtbmlmdHktbmFzZGFxLWdsb2JhbC1tYXJrZXQtdHJlbmRzLWFuZC1hc2lhbi1tYXJrZXQtdXBkYXRlLTc0NDUx0gEA?oc=5" target="_blank">Share Market Updates: 3% बढ़त के साथ बाजार बंद, सेंसेक्स 1700 अंक चढ़ा, 17300 के पार निफ्टी</a>&nbsp;&nbsp;<font color="#6f6f6f">Zee Business हिंदी</font></li><li><a href="https://news.google.com/__i/rss/rd/articles/CBMie2h0dHBzOi8vaGluZGkubmV3czE4LmNvbS9uZXdzL2J1c2luZXNzL3N0b2NrLW1hcmtldC1jbG9zaW5nLXNlbnNleC1qdW1wZWQtYnktMTcwMC1wb2ludHMtbmlmdHktYWxzby1yaXNlcy1zYW1wLTQwMTE5NTcuaHRtbNIBAA?oc=5" target="_blank">Stock Market: शेयर बाजार में जबरदस्त तेजी, Sensex 1700 अंक उछलकर हुआ बंद, निफ्टी 17300 के पार</a>&nbsp;&nbsp;<font color="#6f6f6f">News18 हिंदी</font></li><li><a href="https://news.google.com/__i/rss/rd/articles/CBMipwFodHRwczovL2hpbmRpLm1vbmV5Y29udHJvbC5jb20vbmV3cy9vcGluaW9uL3NoYXJlLW1hcmtldC1saXZlLXVwZGF0ZXMtc3RvY2stbWFya2V0LXRvZGF5LWZlYi0xNS1sYXRlc3QtbmV3cy1ic2UtbnNlLXNlbnNleC1uaWZ0eS1jb3JvbmF2aXJ1cy1yaWwtY2lwbGEtYmhlbC00NDcxOTEuaHRtbNIBAA?oc=5" target="_blank">Closing Bell: सेसेंक्स 1736 अंक चढ़ा, निफ्टी 17300 के ऊपर हुआ बंद, ऑटो, बैंक, मेटल, आईटी शेयर में रह</a>&nbsp;&nbsp;<font color="#6f6f6f">मनी कंट्रोल</font></li><li><a href="https://news.google.com/__i/rss/rd/articles/CBMilQFodHRwczovL25hdmJoYXJhdHRpbWVzLmluZGlhdGltZXMuY29tL25hdmJoYXJhdGdvbGQvZWNvbm9teS9zaGFyZS1tYXJrZXQtbmV3cy11cGRhdGVzLWp1bXAtaW4tc2Vuc2V4LW5zZS1ic2Utc3RvY2stbWFya2V0LWluLWhpbmRpL3N0b3J5Lzg5NTk1NjgxLmNtc9IBAA?oc=5" target="_blank">यूक्रेन बॉर्डर से खुशखबरी, सेंसेक्स में रेकॉर्ड उछाल</a>&nbsp;&nbsp;<font color="#6f6f6f">नवभारत टाइम्स</font></li><li><strong><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lqcDdqckJCRS1oVlRHdzlSMU95Z0FQAQ?oc=5" target="_blank">Google समाचार पर पूरी खबर देखें</a></strong></li></ol>'}

```

------------------------------------------------------------------------------------------------------------------------------------------------------------

## Scrape results from google search
```
gs = GSearch(use_proxy_param=False,use_session=True)

query = "Cooking" ## search term 

query,search_type,site,page_count = query, "" , "twitter.com" , 5

query_urls = gs._generate_urls_(query,search_type,page_count,site=site)

query_results = gs.get_results(query_urls[0:1])

## query results looks like 

[{'title': '#cooking - Twitter Search / Twitter',
  'description': '#cooking - Twitter Search / Twitterhttps://twitter.com › hashtag › cookinghttps://twitter.com › hashtag › cookingSee Tweets about #cooking on Twitter. ... Cooking Channel serves up a world of global cuisines and cooking techniques -- for Food People, by Food People.',
  'links': ['https://twitter.com/hashtag/cooking']},
 {'title': 'Cooking Channel (@CookingChannel) / Twitter',
  'description': 'Web resultsCooking Channel (@CookingChannel) / Twitterhttps://twitter.com › cookingchannelhttps://twitter.com › cookingchannelFrom the people who brought you Food Network, Cooking Channel serves up a world of global cuisines and cooking techniques -- for Food People,\xa0...07-Feb-2022',
  'links': ['https://twitter.com/cookingchannel']},
 {'title': 'NYT Cooking and Food (@nytfood) / Twitter',
  'description': 'NYT Cooking and Food (@nytfood) / Twitterhttps://twitter.com › nytfoodhttps://twitter.com › nytfood23 hours ago — The savviest home cooks and recipe creators always think about how to streamline and innovate in ways big and small, and these 24 baking recipes illustrate just\xa0...',
  'links': ['https://twitter.com/nytfood']}]

```

## Contribution
Contributions are welcome! Feel free to open issues or submit pull requests to enhance the functionality or add new features.


## Contact
For any questions or suggestions, please reach out to [Sunny Raj](https://www.linkedin.com/in/sunny-raj-74631416b/) or create an issue on the repository.

# ***With Google_News_and_SearchScrapper, you have the power to harness Google’s search and news capabilities right at your fingertips. Happy scraping!***
