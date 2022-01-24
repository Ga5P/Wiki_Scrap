import os
import pandas as pd


from bs4 import BeautifulSoup


from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())




wiki = 'https://en.wikipedia.org{link}'

# segment dédié au nombre de résultats
url_search = '/w/index.php?title=Special:Search&limit=1000&'
# segment dédié aux filtres de la recherche
url_filter = '&ns0=1&search=list+intitle%3Arussia%3Brussian&advancedSearch-current=%7B%22fields%22:%7B%22intitle%22:%22russia;russian%22,%22plain%22:[%22list%22]%7D%7D'

n_max_result = 3242

# on parcourt le nombre de résults du début à la fin, par paliers de 1000
list_offset = range(0, n_max_result, 1000)
list_offset = [f"offset={i}" for i in list_offset] #génère liste de caractères dynamiques

list_url = [f"{url_search}{i}{url_filter}" for i in list_offset]
list_url = [wiki.format(link=i) for i in list_url]

all_url = []

for url in list_url:
    driver.get(url)

    content = driver.page_source
    soup = BeautifulSoup(content)

    for i in soup.findAll('div',{'class':'mw-search-result-heading'}):
        ## ce qui est borné par la balise a au sein de la classe parent (div-class-mwsearch)
        title = i.find('a').get('title')
        href = i.find('a').get('href')
        
        info = (title, href)
        all_url.append(info)
        
        
urls = [wiki.format(link=i[1]) for i in all_url]



dfs = [pd.read_html(i,attrs={"class": "wikitable"}) for i in urls]
