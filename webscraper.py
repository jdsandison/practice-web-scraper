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
    global makes, models, ad_id
    
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

    #print(id_values, makes, models)


def manufacture_link(advert_base_url, id):
    return advert_base_url + "/ad/" + str(id)


def advert_info(url, makes, models, id_values):
    get_info(url)
    specs_list = []
    columns = ["Make", "Model", "Ad_ID", "Wheel drive", "Doors", "Seats", "Engine power", "Top speed", "Acceleration (0-62 mph)", "CO2 rating", "Annual tax"]
    df = pd.DataFrame(columns=columns)
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
            
        df_updated = df.copy()    
        for i in range(len(id_values)):
            values_to_write = [specs.get(info, '') for info in columns[3:]]
            df_row = dict(zip(columns[3:], values_to_write))
            df_row['Make'] = makes[i]
            df_row['Model'] = models[i]
            df_row['Ad_ID'] = id_values[i]
            df_updated = pd.concat([df_updated, pd.DataFrame([df_row])], ignore_index=True)    

        if 'Annual tax' in specs:
            df['Annual tax'] = df['Annual tax'].str.replace('£', '')
    
        print(df_updated)

def main():
    base_url = 'https://www.exchangeandmart.co.uk/used-cars-for-sale/under-1-miles-from-dn3-3eh/page'
    page_number = 1

    while True:
        current_url = base_url + str(page_number)
        soup = get_soup(current_url)

        if not soup.find("div", class_="result-item"):
            break

        advert_info(current_url, makes, models, id_values)
        page_number += 1



if __name__ == "__main__":
    main()