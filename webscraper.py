from requests_html import HTMLSession
from bs4 import BeautifulSoup

s = HTMLSession()
url = 'https://books.toscrape.com/'

def getData(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def getTitles(soup):
    titles = soup.find_all('a', {'title': True})
    return [title.get('title') for title in titles]

print(getTitles(getData(url)))