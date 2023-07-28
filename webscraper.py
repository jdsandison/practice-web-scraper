import csv
import requests
from bs4 import BeautifulSoup

url = 'https://www.autotrader.co.uk/car-search?postcode=SW1A%200AA&make=&include-delivery-option=on&advertising-location=at_cars&page=1'

def scrape_autotrader(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    car_details = []
    search_results = soup.find_all("li", class_="search-page__result")
    for result in search_results:
        make = result.find("h2", class_="listing-title").text.strip()
        price = result.find("div", class_="vehicle-price").text.strip()
        car_details.append({"make": make, "price": price})

    return car_details

scraped_data = scrape_autotrader(url)
for car in scraped_data:
    print(f"Make: {car['make']}, Price: {car['price']}")
    
print("hello world!")