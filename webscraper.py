import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 "
                  "Safari/537.36"}


data_file = pd.read_csv(r'data.csv')


def get_soup(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def create_url(advert_base_url, id):
    return advert_base_url + "/ad/" + str(id)


def advert_info(url, current_id):
    first_data = {'makes and models': None,
                  'Id value': current_id}

    full_table_data = []
    accepted_ids = []
    rejected_ids_for_spec = []

    specs_list = []
    accumulated_data = []
    types_of_data = ['Year', 'Engine size', 'Mileage', 'Fuel type', 'Transmission', 'Colour', 'Body type', 'Mpg']
    soup = get_soup(url)
    specs = {}
    make_and_model = soup.find('h2', class_='col-xs-9').find('span', class_='ttl')
    first_data['makes and models'] = make_and_model.get_text(strip=True)
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
        return

    specification_tab_dataframe = pd.DataFrame(specs_list)
    table_data_dataframe = pd.DataFrame(full_table_data)
    table_data_dataframe.columns = types_of_data
    wanted_columns = ['Year', 'Engine size', 'Mileage',
                      'Fuel type', 'Transmission', 'Colour', 'Body type', 'Mpg',
                      'Wheel drive', 'Doors', 'Seats', 'Engine power', 'Top speed',
                      'Acceleration (0-62 mph)', 'CO2 rating', 'Tank range']
    specification_tab_dataframe = specification_tab_dataframe.filter(items=wanted_columns)
    make_and_model_and_id_df = pd.DataFrame(first_data, index=[0])

    for index, row in specification_tab_dataframe.iterrows():
        if row.isna().any():
            print('full spec data is not present')
            return

    combined_dataframe = pd.concat([make_and_model_and_id_df, table_data_dataframe, specification_tab_dataframe],
                                   axis=1, ignore_index=True)

    if combined_dataframe.shape[1] == 18:
        combined_dataframe.columns = ['Make and model', 'ID values', 'Year', 'Engine size', 'Mileage',
                                      'Fuel type', 'Transmission', 'Colour', 'Body type', 'Mpg',
                                      'Wheel drive', 'Doors', 'Seats', 'Engine power', 'Top speed',
                                      'Acceleration (0-62 mph)', 'CO2 rating', 'Tank range']

        return combined_dataframe


def main():
    still_searching = True
    max_consecutive_inactive_ids = 50
    current_consecutive_inactive_ids = 0
    base_url = 'https://www.exchangeandmart.co.uk/ad/'
    data_file_column_length = len(data_file['ID values']) - 1
    current_id_number = data_file.iat[data_file_column_length, data_file.columns.get_loc('ID values')] + 1
    updated_data = data_file

    while still_searching:
        if current_consecutive_inactive_ids > max_consecutive_inactive_ids:
            updated_data.to_csv('data-test.csv', index=False, encoding='utf-8')
            still_searching = False
        else:
            soup = get_soup(base_url + str(current_id_number))
            if soup.find("div", id="vehicle-desc"):
                current_consecutive_inactive_ids = 0
                print(advert_info(base_url + str(current_id_number), current_id_number), current_id_number)
                updated_data = pd.concat([updated_data, advert_info(base_url + str(current_id_number),
                                                                    current_id_number)], axis=0, ignore_index=True)
                current_id_number += 1
            else:
                current_consecutive_inactive_ids += 1
                current_id_number += 1


if __name__ == "__main__":
    main()