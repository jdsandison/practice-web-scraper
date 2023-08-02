import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

makes = []
models = []
id_values = []


def get_soup(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_info(search_url):
    global makes, models, id_values
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

    first_set_of_data = {
        'Makes': makes,
        'Models': models,
        'ID values': id_values
    }
    first_dataframe = pd.DataFrame(first_set_of_data)

    return first_dataframe


def manufacture_link(advert_base_url, id):
    return advert_base_url + "/ad/" + str(id)


def advert_info(url, first_dataframe):
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

        if specs:
            specs_list.append(specs)

    second_dataframe = pd.DataFrame(specs_list)

    big_dataframe = pd.concat([first_dataframe, second_dataframe], axis=1)

    big_dataframe.to_csv('data.csv', index=False, encoding='utf-8')

    #print(second_dataframe)
    #second_dataframe.to_csv('data.csv', index=False, encoding='utf-8')

    # with open("specs.csv", "w", newline="") as csvfile:
    #     info_included = ["Wheel drive", "Doors", "Seats", "Engine power", "Top speed", "Acceleration (0-62 mph)", "CO2 rating", "Annual tax"]
    #     writer = csv.writer(csvfile)
    #     writer.writerow(info_included)
    #     for specs in specs_list:
    #         values_to_write = []
    #
    #         for info in info_included:
    #             value = specs.get(info, '')
    #             if info == 'Annual tax':
    #                 value = value.replace('£', '')
    #             values_to_write.append(value)
    #
    #         writer.writerow(values_to_write)


def main():
    base_url = 'https://www.exchangeandmart.co.uk/used-cars-for-sale/under-1-miles-from-dn3-3eh/page'
    page_number = 1
    max_page = 3

    while True:
        current_url = base_url + str(page_number)
        soup = get_soup(current_url)

        if not soup.find("div", class_="result-item"):
            break

        if page_number > max_page:
            break

        first_dataframe = get_info(current_url)
        advert_info(current_url, first_dataframe)
        page_number += 1


if __name__ == "__main__":
    main()