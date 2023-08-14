import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

makes = []
models = []
id_values = []


def get_soup(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_page_info(search_url):
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

    search_data = {
        'Makes': makes,
        'Models': models,
        'ID values': id_values
    }

    search_dataframe = pd.DataFrame(search_data)

    return search_dataframe


def create_url(advert_base_url, id):
    return advert_base_url + "/ad/" + str(id)


def advert_info():

    full_table_data = []
    accepted_ids = []

    specs_list = []
    accumulated_data = []
    table_data_dataframe = pd.DataFrame()
    for i in range(0, len(id_values)):
        current_advert_link = create_url("https://www.exchangeandmart.co.uk", id_values[i])
        soup = get_soup(current_advert_link)
        specs = {}
        specification_tab = soup.find_all("div", class_="adSpecItem")
        table_of_info = soup.find_all("div", class_="adDetsItem")
        for item in specification_tab:
            data = list(item.stripped_strings)
            key = data[0].strip(':')
            value = data[1]
            specs[key] = value

        if specs:
            specs_list.append(specs)

        types_of_data = ['Accepted id value', 'Year', 'Engine size', 'Mileage', 'Fuel type', 'Transmission', 'Colour', 'Body type', 'Mpg']
        list_of_table_data = []
        for info in table_of_info:
            data = info.text.strip()
            list_of_table_data.append(data)

        if len(list_of_table_data) == 8:
            accepted_ids.append(id_values[i])
            accumulated_data.append(list_of_table_data)
            full_table_data.append(accumulated_data[-1])
        else:
            print('not all data present', list_of_table_data, 'rejected id value', id_values[i])

    specification_tab_dataframe = pd.DataFrame(specs_list)
    table_data_dataframe = pd.DataFrame(full_table_data)
    accepted_ids_dataframe = pd.DataFrame(accepted_ids)
    table_data_and_id_dataframe = pd.concat([accepted_ids_dataframe, table_data_dataframe], axis=1)
    table_data_and_id_dataframe.columns = types_of_data
    #print(table_data_and_id_dataframe)
    specification_tab_and_id = pd.concat([accepted_ids_dataframe, specification_tab_dataframe], axis=1)
    specification_tab_and_id = specification_tab_dataframe.drop(columns=['Boot capacity', 'Delivery', 'Insurance', 'Annual tax'])
    print(specification_tab_and_id)


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

        first_dataframe = get_page_info(current_url)

        page_number += 1

    advert_info()


if __name__ == "__main__":
    main()