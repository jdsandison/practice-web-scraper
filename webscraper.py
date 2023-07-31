import requests
from bs4 import BeautifulSoup
import csv
import json

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}


def get_soup(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_info(search_url):
    soup = get_soup(search_url)
    div_elements = soup.find_all("div", class_="result-item")

    makes = []
    models = []
    id_values = []

    for div in div_elements:
        makes.append(div.get("make", "Unknown make"))
        models.append(div.get("model", "Unknown model"))
        id_values.append(div.get("adid", "Unknown id"))

    print(makes)

def main():
    base_url = 'https://www.exchangeandmart.co.uk/used-cars-for-sale/under-1-miles-from-dn3-3eh/page'
    page_number = 1

    while True:
        current_url = base_url + str(page_number)
        soup = get_soup(current_url)

        if not soup.find("div", class_="result-item"):
            break

        get_info(current_url)
        page_number += 1



if __name__ == "__main__":
    main()