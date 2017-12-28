
# coding: utf-8

# # Scraper in Python
# ## Requirements
# - ## Urllib2 ( python 2.x ), Urllib (python 3)
# - ## BeautifulSoup (beautifulsoup4)
# - ## Requests
# - ## Pandas
# - ## Selenium
# - ## Sqlite3

# # How to install the package
# 
# ## Using pip
# - ### pip install beautifulsoup4
# - ### pip install requests
# - ### pip install pandas

# In[1]:


import sys
if sys.version_info>(3,0):
    from urllib.request import urlopen
else:
    from urllib2 import urlopen
from bs4 import BeautifulSoup
import requests


# In[2]:


#test packages
print (urlopen)
print (BeautifulSoup)
print (requests.__version__)


# # urlopen
# ## Open the URL url, which can be either a string or a Request object.

# In[3]:


html = urlopen('http://www.nccu.edu.tw/')
content = html.read()
print (content)


# In[4]:


if sys.version_info>(3,0):
    title = content.decode().split('<title>')[1].split('</title')[0]
else:
    title = content.split('<title>')[1].split('</title')[0]
print (title)


# # BeautifulSoup
# ## The term Beautiful Soup originates with Lewis Carroll's Alice's Adventures in Wonderland and a song Beautiful Soup
# ## Beautiful Soup is a Python library for pulling data out of HTML and XML files

# In[5]:


soup = BeautifulSoup(content)
print (soup.prettify())


# In[6]:


print (soup.title)
print (soup.title.name)
print (soup.title.text)
print (soup.title.string)
print (soup.title.get_text())
print (soup.title.parent.name)
print (soup.title.parent.parent.name)
print (soup.title.child)


# # find( ) : find the first element
# # find_all( ) : find all element

# In[7]:


about_nccu = soup.find_all('ul',{'class':'page_menu level_2'})[0]
output= about_nccu.get_text()
print (about_nccu)
print (output)


# In[8]:


about_nccu2 = soup.find_all('ul',{'class':'page_menu level_2'})[0].find_all('a')
print (about_nccu2)
print (about_nccu2[0]['href'])
print (about_nccu2[0].get_text())


# In[9]:


about_nccu3 = soup.find_all('a',{'data-menu-link':'true'})[1:7]
print (about_nccu3)
print ([x['href'] for x in about_nccu3][0])
print ([x.get_text() for x in about_nccu3][0])


# # HTTP vs. HTTPS

# In[10]:


if sys.version_info>(3,0):
    from urllib.error import HTTPError
else:
    from urllib2 import HTTPError

try:
    ptt = urlopen('https://www.ptt.cc/bbs/movie/M.1513345790.A.174.html')
except HTTPError as e:
    print (e)


# # User-agent
# ## Mozilla/5.0
# ## python urllib/x.x.x

# In[11]:


if sys.version_info>(3,0):
    from urllib.request import Request
else:
    from urllib2 import Request

ptt = urlopen(Request('https://www.ptt.cc/bbs/movie/M.1513345790.A.174.html' ,headers={'User-Agent' : "Mozilla/5.0"}))
html = ptt.read()
print (html)


# In[12]:


html = requests.get('https://www.ptt.cc/bbs/movie/index.html')
print (html.content)


# ## Traveling the website

# In[15]:


import re

first_webpage = 'https://en.wikipedia.org/wiki/National_Chengchi_University'
quene = [first_webpage]
history = list()

#do recursive
web_page = quene.pop(0)
history.append(web_page)
html = requests.get(web_page)
soup = BeautifulSoup(html.content)
urls = soup.findAll('a', href=re.compile("^/wiki/"))
for url in urls:
    new_webpage = 'https://en.wikipedia.org'+url['href'] 
    if new_webpage not in history:
        quene.append(new_webpage)
print (quene,history)


# # HTTP METHOD
# ## GET vs POST
# ## Get: 明信片
# ## Post: 信封

# In[16]:


#google map (get)
json_data = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng=25.033493,121.564101')
print (json_data.content)


# In[17]:


#PCHome
pc_home = requests.get('https://ecshweb.pchome.com.tw/search/v3.3/?q=notebook')
print (pc_home.content)


# In[18]:


import json

pc_home_page = requests.get('https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=notebook&page=1&sort=rnk/dc')
pc_home_page = json.loads(pc_home_page.content)
for prod in (pc_home_page)['prods']:
    print (prod['name'])


# In[31]:


#high speed rail (post)
params = {'StartStation':'2f940836-cedc-41ef-8e28-c2336ac8fe68',
          'EndStation':'977abb69-413a-4ccf-a109-0272c24fd490',
          'SearchDate':'2017/12/30',
          'SearchTime':'15:00',
          'SearchWay':'DepartureInMandarin'}
r = requests.post("http://www.thsrc.com.tw/tw/TimeTable/SearchResult",data=params)
print (r.content)


# In[33]:


soup = BeautifulSoup(r.content)
trips = soup.find_all('td',{'class':'column1'})
print ([x.get_text() for x in trips])


# # Redirect

# In[34]:


params = {'datestart':'2017/12/18',
          'dateend':'2017/12/19',
          'COMMODITY_ID':'I5F',
          'his_year':'2016',          
          }
r = requests.post("http://www.taifex.com.tw/chinese/3/3_1_2dl.asp",data=params)
print (r.headers)


# In[35]:


print (r.history[0].headers['location'])


# # Sessions & Cookies
# 

# In[36]:


cookie = {'over18':'1'}
r = requests.get('https://www.ptt.cc/bbs/Gossiping/index.html',cookies=cookie)
print (r.content)


# # Use pandas to read html tables
# - ## pandas.read_html

# In[37]:


from IPython.display import display
import pandas as pd
stock_id = "2451"
res = requests.get("http://tw.stock.yahoo.com/d/s/major_%s.html" % stock_id)
tables = pd.read_html(res.text)


# In[38]:


display(tables[9])


# In[39]:


table = tables[9]
#zip(table[:][0], table[:][1], table[:][2])
new_table = ([ [a,b,c,d] for a,b,c,d in zip(table[1:][0], table[1:][1], table[1:][2], table[1:][3]) ] + 
             [ [a,b,c,d] for a,b,c,d in zip(table[1:][4], table[1:][5], table[1:][6], table[1:][7]) ])
df = pd.DataFrame(new_table)
df.columns = ['name', 'buy', 'sell', 'oversold']
display(df)


# # Example
# ## https://boardgamegeek.com/browse/boardgame
# ## Target
# - ### Board name
# - ### Url
# - ### Rating
# - ### Description
# # Using Sqlite to store the data

# In[40]:


page = 1
r= requests.get('https://boardgamegeek.com/browse/boardgame/page/%d' % page)
print (r.content)


# In[41]:


page = 1
r= requests.get('https://boardgamegeek.com/browse/boardgame/page/%d' % page)
soup = BeautifulSoup(r.content,'lxml')
tables = soup.find_all(id="row_")
print (len(tables))
print (tables[0])


# In[42]:


links = list()
for table in tables:
    link = 'https://boardgamegeek.com' + table.find_all('a')[1]['href']
    links.append(link)
print (links[0])


# In[29]:


from selenium import webdriver

link = links[0]
driver = webdriver.PhantomJS(executable_path='./phantomjs.exe')
driver.get(link)
pageSource = driver.page_source
driver.close()  
soup_subpage = BeautifulSoup(pageSource,'lxml')
print (soup_subpage)


# In[30]:


# Board name
print (soup_subpage.find_all('a',{'ui-sref':'geekitem.overview'}))
print (soup_subpage.find_all('a',{'ui-sref':'geekitem.overview'})[1].text.replace('\t','').strip())


# In[31]:


# url
print (link)


# In[32]:


#rating
print (soup_subpage.find_all('span', {'ng-show':'showRating'})[0].text.replace('\t','').strip())


# In[33]:


# Description
print (soup_subpage.find('meta', {'name':'description'})['content'])


# In[34]:


import sqlite3

conn = sqlite3.connect('boardgame.sqlite')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE boardgame
                  ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    board_name CHAR(256) NOT NULL,
                    url CHAR(256) NOT NULL,
                    rating CHAR(256) NOT NULL,
                    description text NOT NULL
                    );''')
conn.commit()
conn.close()


# In[35]:


board_name = soup_subpage.find_all('a',{'ui-sref':'geekitem.overview'})[1].text.replace('\t','').replace('"','\'').strip()
url = link
rating = soup_subpage.find_all('span', {'ng-show':'showRating'})[0].text.replace('\t','').strip()
description = soup_subpage.find('meta', {'name':'description'})['content']
conn = sqlite3.connect('boardgame.sqlite')
cursor = conn.cursor()
command = "INSERT INTO boardgame (board_name, url, rating, description) VALUES (\'%s\', \'%s\', \'%s\', \"%s\");" % (board_name, url, rating, description)
cursor.execute(command)
conn.commit()
conn.close()


# In[46]:


from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import random
import sqlite3

conn = sqlite3.connect('boardgame.sqlite')
cursor = conn.cursor()
#build database
cursor.execute('''CREATE TABLE boardgame
                  ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    board_name CHAR(256) NOT NULL,
                    url CHAR(256) NOT NULL,
                    rating CHAR(256) NOT NULL,
                    description text NOT NULL
                    );''')
conn.commit()
#total_page = 956
total_page = 1
for page in range(1,total_page+1):
    #main_page
    r_mainpage= requests.get('https://boardgamegeek.com/browse/boardgame/page/%d' % page)
    soup_mainpage = BeautifulSoup(r_mainpage.content,'lxml')
    tables = soup.find_all(id="row_")
    #get_links
    links = list()
    for table in tables:
        url = 'https://boardgamegeek.com' + table.find_all('a')[1]['href']
        links.append(url)
    #get each subpage    
    for link in links[:10]:
        driver = webdriver.PhantomJS(executable_path='./phantomjs.exe')
        driver.get(link)
        pageSource = driver.page_source
        driver.close()  
        soup_subpage = BeautifulSoup(pageSource,'lxml')
        #get features
        board_name = soup_subpage.find_all('a',{'ui-sref':'geekitem.overview'})[1].text.replace('\t','').replace('"','\'').strip()
        url = link
        rating = soup_subpage.find_all('span', {'ng-show':'showRating'})[0].text.replace('\t','').strip()
        description = soup_subpage.find('meta', {'name':'description'})['content']
        #sql insert
        command = "INSERT INTO boardgame (board_name, url, rating, description) VALUES (\'%s\', \'%s\', \'%s\', \"%s\");" % (board_name, url, rating, description)
        cursor.execute(command)
        conn.commit()
        time.sleep(2)
conn.close()


# In[47]:


conn = sqlite3.connect('boardgame.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT * FROM boardgame")
row = cursor.fetchall()
conn.close()
print (len(row))

