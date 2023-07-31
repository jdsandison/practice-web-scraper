import requests
from bs4 import BeautifulSoup
import csv

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}


def find_listings(search_url):
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    car_titles = soup.find_all("p", attrs={"data-testid": "search-listing-subtitle", "class": "sc-kcuKUB sc-fWFeAW gZMaoW VTOnK"})
    for title in car_titles:
        car_title = title.text.strip()
        print(car_title)

def main():
    search_url = 'https://www.autotrader.co.uk/car-search?postcode=SW1A%200AA&make=&include-delivery-option=on&advertising-location=at_cars&page=1'
    find_listings(search_url)

if __name__ == "__main__":
    main()