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


def more_info(url):
    soup = get_soup(url)
    list_of_extra_info = []
    extra_info = soup.find_all("div", class_="adDetsItem")
    types_of_data = ['Year', 'Engine size', 'Mileage', 'Fuel type', 'Transmission', 'Colour', 'Body type', 'Mpg']

    for info in extra_info:
        data = info.text.strip()
        print(data)
        # regex
        year_pattern = re.compile(r'(\d+(\.\d+)?)(L)')
        engine_size_pattern = re.compile(r'(\d+(\.\d+)?)(L)')
        mileage_pattern = re.compile(r'(\d{1,3}(,\d{3})*(\.\d+)?)(\s*)miles')
        fuel_type_pattern = re.compile(r'(Petrol|Diesel|Hybrid|Electric)')
        transmission_pattern = re.compile(r'(manual|automatic|semiauto)', re.IGNORECASE)
        color_pattern = re.compile(r'(red|blue|green|black|white|silver|grey|pink|yellow|orange|purple)', re.IGNORECASE)
        body_type_pattern = re.compile(r'(hatchback|suv|coupe|covertible)', re.IGNORECASE)
        mpg_pattern = re.compile(r'(\d+(\.\d+)?)\s*mpg')

        # Extracting the data
        year = re.search(year_pattern, data).group(1) if re.search(year_pattern, data) else None
        engine_size = re.search(engine_size_pattern, data).group(1) if re.search(engine_size_pattern, data) else None
        mileage = re.search(mileage_pattern, data).group(1) if re.search(mileage_pattern, data) else None
        fuel_type = re.search(fuel_type_pattern, data).group(1) if re.search(fuel_type_pattern, data) else None
        transmission = re.search(transmission_pattern, data).group(1) if re.search(transmission_pattern, data) else None
        color = re.search(color_pattern, data).group(1) if re.search(color_pattern, data) else None
        body_type = re.search(body_type_pattern, data).group(1) if re.search(body_type_pattern, data) else None
        mpg = re.search(mpg_pattern, data).group(1) if re.search(mpg_pattern, data) else None

    info_dict = {
        'Year': year,
        'Engine size': engine_size,
        'Mileage': mileage,
        'Fuel type': fuel_type,
        'Transmission': transmission,
        'Colour': color,
        'Body type': body_type,
        'Mpg': mpg
    }

    #print(info_dict)

    extra_dataframe = pd.DataFrame(list_of_extra_info)

    return extra_dataframe


def temp_function():
    bigger_dataset = pd.DataFrame()
    for i in range(len(id_values)):
        current_advert_link = manufacture_link("https://www.exchangeandmart.co.uk", id_values[i])
        #print(current_advert_link)
        smaller_dataset = more_info(current_advert_link)
        bigger_dataset = pd.concat([bigger_dataset, smaller_dataset], axis=0)

    return bigger_dataset


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

        #advert_info(current_url, first_dataframe)

        temp_function()
        page_number += 1


if __name__ == "__main__":
    main()