from requests_html import HTMLSession
from bs4 import BeautifulSoup

s = HTMLSession()
url = 'https://books.toscrape.com/catalogue/page-1.html'
base_url = 'https://books.toscrape.com/catalogue/page-{}.html'
all_titles = []


def getData(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def getTitles(soup):
    titles = soup.find_all('a', {'title': True})
    return [title.get('title') for title in titles]


for page_number in range(1, 51):
    page_url = base_url.format(page_number)
    titles = getTitles(getData(page_url))
    all_titles.extend(titles)

print(len(all_titles))


def testing():
    for i in range(5):
        print(len(all_titles))

           
print(testing())