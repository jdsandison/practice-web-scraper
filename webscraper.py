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
    for div in div_elements:
        makes = [div["make"]]
        models = [div["model"]]
        id_values = [div["adid"]]
        print(makes, models, id_values)

def main():
    search_url = 'https://www.exchangeandmart.co.uk/used-cars-for-sale/any-distance-from-dn3-3eh'
    get_info(search_url)


if __name__ == "__main__":
    main()