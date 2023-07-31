import requests
from bs4 import BeautifulSoup
import csv
import json

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

makes = []
models = []
id_values = []

def get_soup(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_info(search_url):
    soup = get_soup(search_url)
    div_elements = soup.find_all("div", class_="result-item")

    for div in div_elements:
        makes.append(div.get("make", "Unknown make"))
        models.append(div.get("model", "Unknown model"))
        id_values.append(div.get("adid", "Unknown id"))


def manufacture_link(advert_base_url, id):
    return advert_base_url + "/ad/" + str(id)


def advert_info(url):
    info_dictionary = {
        'wheel_drive': 0,
        'doors': 0,
        'seats': 0,
        'boot_capacity': 0,
        'engine_power': 0,
        'top_speed': 0,
        'acceleration': 0,
        'co2': 0,
        'range_of_tank': 0,
        'tax': 0}
    for i in range(0, len(id_values)):
        current_advert_link = manufacture_link("https://www.exchangeandmart.co.uk/", id_values[i])
        soup = get_soup(current_advert_link)

        div_elements = soup.find_all("div", class_="adSpecItem")
        div_elements.pop()
        
        keys_to_update = ['wheel_drive', 'doors', 'seats', 'boot_capacity', 'engine_power', 'top_speed', 'acceleration', 'co2', 'range_of_tank', 'tax']
        for key, value in zip(keys_to_update, div_elements):
            info_dictionary[key] = value

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