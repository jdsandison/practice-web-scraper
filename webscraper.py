import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

makes = []
models = []
id_values = []

data_file = pd.read_csv(r'data.csv')


def get_soup(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


# def get_page_info(search_url):
#     global makes, models, id_values
#     soup = get_soup(search_url)
#     div_elements = soup.find_all("div", class_="result-item")
#
#     for div in div_elements:
#         make = (div.get("make", "Unknown make"))
#         model = (div.get("model", "Unknown model"))
#         ad_id = (div.get("adid", "Unknown id"))
#
#         if make != "Unknown make" and model != "Unknown model" and ad_id != "unknown id":
#             makes.append(make)
#             models.append(model)
#             id_values.append(ad_id)
#
#     search_data = {
#         'Makes': makes,
#         'Models': models,
#         'ID values': id_values
#     }
#
#     search_dataframe = pd.DataFrame(search_data)
#
#     return search_dataframe


def create_url(advert_base_url, id):
    return advert_base_url + "/ad/" + str(id)


def advert_info(url, current_id):

    full_table_data = []
    accepted_ids = []
    rejected_ids_for_spec = []

    specs_list = []
    accumulated_data = []
    types_of_data = ['Accepted id value', 'Year', 'Engine size', 'Mileage', 'Fuel type', 'Transmission', 'Colour', 'Body type', 'Mpg']
    soup = get_soup(url)
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
        print('no given specification tab', current_id)
        rejected_ids_for_spec.append(current_id)

    list_of_table_data = []
    for info in table_of_info:
        data = info.text.strip()
        list_of_table_data.append(data)

    if len(list_of_table_data) == 8:
        accepted_ids.append(current_id)
        accumulated_data.append(list_of_table_data)
        full_table_data.append(accumulated_data[-1])
    else:
        print('not all data present', list_of_table_data, 'rejected id value', current_id)

    specification_tab_dataframe = pd.DataFrame(specs_list)
    table_data_dataframe = pd.DataFrame(full_table_data)
    accepted_ids_dataframe = pd.DataFrame(accepted_ids)
    table_data_and_id_dataframe = pd.concat([accepted_ids_dataframe, table_data_dataframe], axis=1)
    table_data_and_id_dataframe.columns = types_of_data
    specification_tab_and_id = pd.concat([accepted_ids_dataframe, specification_tab_dataframe], axis=1)
    wanted_columns = ['Makes', 'Models', 'ID values', 'Year', 'Engine size', 'Mileage',
                  'Fuel type', 'Transmission', 'Colour', 'Body type', 'Mpg',
                  'Wheel drive', 'Doors', 'Seats', 'Engine power', 'Top speed',
                  'acceleration', 'CO2 rating', 'Tank range']
    specification_tab_and_id = specification_tab_and_id.filter[wanted_columns]

    for advert_id in rejected_ids_for_spec:
        rows_to_drop_table = table_data_and_id_dataframe[table_data_and_id_dataframe.iloc[:, 0] == advert_id].index
        rows_to_drop_specification = specification_tab_and_id[specification_tab_and_id.iloc[:, 0] == advert_id].index
        table_data_and_id_dataframe.drop(rows_to_drop_table, inplace=True)
        table_data_and_id_dataframe.reset_index(drop=True, inplace=True)
        specification_tab_and_id.drop(rows_to_drop_specification, inplace=True)
        specification_tab_and_id.reset_index(drop=True, inplace=True)
        print('Dropping rows with', advert_id)

    rows_with_nan_values = []
    for index, row in specification_tab_and_id.iterrows():
        if row.isna().any():
            rows_with_nan_values.append(index)

    print(rows_with_nan_values)
    specification_tab_and_id.drop(rows_with_nan_values, inplace=True)
    specification_tab_and_id.reset_index(drop=True, inplace=True)
    table_data_and_id_dataframe.drop(rows_with_nan_values, inplace=True)
    table_data_and_id_dataframe.reset_index(drop=True, inplace=True)

    table_data_and_id_dataframe = table_data_and_id_dataframe.drop(columns=table_data_and_id_dataframe.columns[0])
    specification_tab_and_id = specification_tab_and_id.drop(columns=specification_tab_and_id.columns[0])

    combined_dataframe = pd.concat([table_data_and_id_dataframe, specification_tab_and_id], axis=1)

    return combined_dataframe


def main():
    still_searching = True
    starting_number = 29000000
    max_consecutive_inactive_ids = 1000
    current_consecutive_inactive_ids = 0
    base_url = 'https://www.exchangeandmart.co.uk/ad/'
    data_file_column_length = len(data_file['ID values']) - 1
    current_id_number = data_file.iat[data_file_column_length, data_file.get_loc('ID values')]

    while still_searching:
        if current_consecutive_inactive_ids > max_consecutive_inactive_ids:
            still_searching = False
        else:
            soup = get_soup(base_url + str(current_id_number))
            if soup.find("div", id="vehicle-desc"):
                current_consecutive_inactive_ids = 0
                data_file.append(advert_info(base_url + str(current_id_number), current_id_number))
                current_id_number += 1
            else:
                current_consecutive_inactive_ids += 1
                current_id_number += 1

    data_file.to_csv("data.csv", index=False, encoding="utf-8")


if __name__ == "__main__":
    main()