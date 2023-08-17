import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

makes = []
models = []
id_values = []
available_makes_filtered = []
ids_of_makes = []
makes2 = []
models2 = []
id_values2 = []


def get_soup(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_car_models(base_url):
    global available_makes_filtered
    soup = get_soup(base_url)
    available_makes_unfiltered = []

    list_of_available_makes = soup.find_all("div", class_="c-column-section")
    list_of_available_makes = list_of_available_makes[1]
    for potential_make in list_of_available_makes:
        make_text = potential_make.text
        available_makes_unfiltered.append(make_text)

    for i in range(len(available_makes_unfiltered)):
        if available_makes_unfiltered[i] == '\n':
            pass
        else:
            available_makes_filtered.append(available_makes_unfiltered[i])

    available_makes_filtered = [brand.replace('Used ', '') for brand in available_makes_filtered]

    for idx, make in enumerate(available_makes_filtered):
        if make in ['Alfa Romeo', 'Aston Martin', 'Land Rover']:
            available_makes_filtered[idx] = make.replace(' ','-')

    return available_makes_filtered


def get_page_info(search_url):
    """
    :param search_url: the url of the listings on a specific page number
    :return: search_dataframe: dataframe containing all the makes, models and id of specific ad pages
    """

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
    """
    :param advert_base_url: base url
    :param id: advert id of specific ads
    :return: the url of the ad page
    """
    return advert_base_url + "/ad/" + str(id)


def removing_nan_values(dataframe):
    rows_with_nan_values = []
    for index, row in dataframe.iterrows():
        if row.isna().any():
            rows_with_nan_values.append(index)

    dataframe.drop(rows_with_nan_values, inplace=True)
    dataframe.reset_index(drop=True, inplace=True)

    return dataframe


def get_ids_of_each_make(make, page_number):
    global ids_of_makes, makes2, models2, id_values2
    temp_id_values = []
    make_url = 'https://www.exchangeandmart.co.uk/used-cars-for-sale/any-distance-from-b30-3aa/' + str(make) + '/page' + str(page_number)
    soup = get_soup(make_url)
    elements = soup.find_all("div", class_="result-item")
    for div in elements:
        make = (div.get("make", "Unknown make"))
        model = (div.get("model", "Unknown model"))
        ad_id = (div.get("adid", "Unknown id"))

        if make != "Unknown make" and model != "Unknown model" and ad_id != "unknown id":
            makes2.append(make)
            models2.append(model)
            temp_id_values.append(ad_id)

        id_values2.append(temp_id_values[-1])
        
    search_data = {
        'Makes': makes2,
        'Models': models2,
        'ID values': id_values2
    }

    #search_dataframe = pd.DataFrame(search_data)

    #return search_dataframe
    return search_data['ID values']


def advert_info():
    """
    function that scrapes data from 2 different sections of the website. The 'table' and the 'specification tab'.

    :return: combined_dataframe: dataframe composed of the 2 sections of data to be scraped
    """

    full_table_data = []
    accepted_ids = []
    rejected_ids_for_spec = []

    specs_list = []
    accumulated_data = []
    types_of_data = ['Accepted id value', 'Year', 'Engine size', 'Mileage', 'Fuel type', 'Transmission', 'Colour', 'Body type', 'Mpg']
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
        else:
            #print('no given specification tab', id_values[i])
            rejected_ids_for_spec.append(id_values[i])

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
    specification_tab_and_id = pd.concat([accepted_ids_dataframe, specification_tab_dataframe], axis=1)
    specification_tab_and_id = specification_tab_and_id.drop(columns=['Boot capacity', 'Delivery', 'Insurance', 'Annual tax'], errors='ignore')

    for advert_id in rejected_ids_for_spec:
        rows_to_drop_table = table_data_and_id_dataframe[table_data_and_id_dataframe.iloc[:, 0] == advert_id].index
        rows_to_drop_specification = specification_tab_and_id[specification_tab_and_id.iloc[:, 0] == advert_id].index
        table_data_and_id_dataframe.drop(rows_to_drop_table, inplace=True)
        table_data_and_id_dataframe.reset_index(drop=True, inplace=True)
        specification_tab_and_id.drop(rows_to_drop_specification, inplace=True)
        specification_tab_and_id.reset_index(drop=True, inplace=True)
        #print('Dropping rows with', advert_id)

    rows_with_nan_values = []
    for index, row in specification_tab_and_id.iterrows():
        if row.isna().any():
            rows_with_nan_values.append(index)

    specification_tab_and_id.drop(rows_with_nan_values, inplace=True)
    specification_tab_and_id.reset_index(drop=True, inplace=True)
    table_data_and_id_dataframe.drop(rows_with_nan_values, inplace=True)
    table_data_and_id_dataframe.reset_index(drop=True, inplace=True)

    table_data_and_id_dataframe = table_data_and_id_dataframe.drop(columns=table_data_and_id_dataframe.columns[0])
    specification_tab_and_id = specification_tab_and_id.drop(columns=specification_tab_and_id.columns[0])

    combined_dataframe = pd.concat([table_data_and_id_dataframe, specification_tab_and_id], axis=1)

    return combined_dataframe


def main():
    base_url = 'https://www.exchangeandmart.co.uk/used-cars-for-sale/any-distance-from-b30-3aa/page'
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

        get_car_models(base_url)
        for make in available_makes_filtered:
            output_ids = get_ids_of_each_make(make, page_number)
            print(output_ids)
            ids_of_makes.append(output_ids)
            print('working!' + make)

        page_number += 1

    print(ids_of_makes)
    print('didnt work')

    # second_dataframe = advert_info()
    #
    # final_dataframe = pd.concat([first_dataframe, second_dataframe], axis=1)
    #
    # rows_with_nan_values = []
    # for index, row in final_dataframe.iterrows():
    #     if row.isna().any():
    #         rows_with_nan_values.append(index)
    #
    # final_dataframe.drop(rows_with_nan_values, inplace=True)
    # final_dataframe.reset_index(drop=True, inplace=True)
    #
    # final_dataframe.to_csv('data.csv', index=False, encoding='utf-8')

if __name__ == "__main__":
    main()