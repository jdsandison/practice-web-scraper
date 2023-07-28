import requests
from bs4 import BeautifulSoup
import csv

def find_listings(search_url):
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")

    listing_links = soup.find_all("a", attrs={"data-testid": "search-listing-title"})
    for link in listing_links:
        car_title = link.find("h3").text.strip()
        print(car_title)

def main():
    search_url = 'https://www.autotrader.co.uk/car-search?postcode=SW1A%200AA&make=&include-delivery-option=on&advertising-location=at_cars&page=1'
    find_listings(search_url)

if __name__ == "__main__":
    main()