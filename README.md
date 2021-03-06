# Crawler
This is the project that I started based on the micro project held by TigerBit.io. 

The goal of this project is to build a web crawler that can crawl at a speed of 100 pages/sec

The detail information of the project can be found on the website: 
http://bittiger.io/

#Project Structure
    .
    ├── README.md
    ├── appstore
    │   ├── __init__.py
    │   ├── __init__.pyc
    │   ├── items.py
    │   ├── items.pyc
    │   ├── list.txt
    │   ├── pipelines.py
    │   ├── pipelines.pyc
    │   ├── random_proxy.py
    │   ├── random_proxy.pyc
    │   ├── random_useragent.py
    │   ├── random_useragent.pyc
    │   ├── settings.py
    │   ├── settings.pyc
    │   └── spiders
    │       ├── __init__.py
    │       ├── __init__.pyc
    │       ├── huawei_spider.py
    │       ├── huawei_spider.pyc
    │       ├── huawei_spider_modified.py
    │       └── huawei_spider_modified.pyc
    ├── appstore.dat
    └── scrapy.cfg

#Key Files
    - items.py: define the type of data to be collected from a specific web crawler. 
      In this case, I am creating a web crawler for huawei appstore. So the
      fields that I define are:
        - title: the title of the app
        - url: the link to the app main page on Huawei appstore
        - appid: the id of the app in the Huawei appstore
        - intro: the description of the app
        - recommend: the recommended apps for users who are interested in the current app provided by Huawei. 
    - pipelines.py: define the format of the data being stored in the file
    - settings.py: define the item pipe for the huawei web crawler, its priority and delay between each crawling request. 

#The Crawlers
- huawei_spider 
    This crawler crawl the page at: http://appstore.huawei.com/more/all
    It scrape all the apps on this page based on the items type defined in the items.py file
- huawei_spider_modified
    This crawler not only crawl the page at: http://appstore.huawei.com/more/all.
    It also go to the page of each app listed there and scrape the info of the recommended apps as well

#Random Proxy and User Agent
- When increase the speed of crawling, the risk of being detected as crawling also increases. Therefore, we need to use random user agent and proxy to go around this problem. 