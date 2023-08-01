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
        make = (div.get("make", "Unknown make"))
        model = (div.get("model", "Unknown model"))
        ad_id = (div.get("adid", "Unknown id"))

        if make != "Unknown make" and model != "Unknown model" and ad_id != "unknown id":
            makes.append(make)
            models.append(model)
            id_values.append(ad_id)

    print(id_values, makes, models)


def manufacture_link(advert_base_url, id):
    return advert_base_url + "/ad/" + str(id)


def advert_info(url):
    get_info(url)
    specs_list = []
    for i in range(0, len(id_values)):
        current_advert_link = manufacture_link("https://www.exchangeandmart.co.uk", id_values[i])
        soup = get_soup(current_advert_link)
        specs = {}
        ad_spec_items = soup.find_all("div", class_="adSpecItem")
        for item in ad_spec_items:
            data = list(item.stripped_strings)
            key = data[0].strip(':')
            value = data[1]
            specs[key] = value
        specs_list.append(specs)

    with open("specs.csv", "w", newline="") as csvfile:
        info_included = ["Wheel drive", "Doors", "Seats", "Engine power", "Top speed", "Acceleration (0-62 mph)", "CO2 rating", "Annual tax"]
        writer = csv.writer(csvfile)
        writer.writerow(info_included)
        for specs in specs_list:
            values_to_write = []

            for info in info_included:
                value = specs.get(info, '')
                if info == 'Annual tax':
                    value = value.replace('£', '')
                values_to_write.append(value)

            writer.writerow(values_to_write)


def main():
    base_url = 'https://www.exchangeandmart.co.uk/used-cars-for-sale/under-1-miles-from-dn3-3eh/page'
    page_number = 1

    while True:
        current_url = base_url + str(page_number)
        soup = get_soup(current_url)

        if not soup.find("div", class_="result-item"):
            break

        advert_info(current_url)
        page_number += 1



if __name__ == "__main__":
    main()