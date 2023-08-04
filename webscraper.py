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
    mega_extra_dataframe = pd.DataFrame()
    specs_list = []
    for i in range(0, len(id_values)):
        current_advert_link = manufacture_link("https://www.exchangeandmart.co.uk", id_values[i])
        soup = get_soup(current_advert_link)
        extra_dataframe = more_info(current_advert_link)
        mega_extra_dataframe = pd.concat([mega_extra_dataframe, extra_dataframe], axis=1)
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

    big_dataframe = pd.concat([first_dataframe, second_dataframe, mega_extra_dataframe], axis=1)

    big_dataframe.to_csv('data.csv', index=False, encoding='utf-8')


def more_info(url):
    soup = get_soup(url)
    list_of_extra_info = []
    my_list = []
    info_dictionary = {}
    extra_info = soup.find_all("div", class_="adDetsItem")
    types_of_data = ['Year', 'Engine size', 'Mileage', 'Fuel type', 'Transmission', 'Colour', 'Body type', 'Mpg']

    for info in extra_info:
        data = info.text.strip()
        my_list.append(data)

    for i in range(len(types_of_data)):
        key = types_of_data[i]
        value = my_list[i]

        info_dictionary[key] = value

    if info_dictionary:
        list_of_extra_info.append(info_dictionary)

    extra_dataframe = pd.DataFrame(list_of_extra_info)

    return extra_dataframe


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