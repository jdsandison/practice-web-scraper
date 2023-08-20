import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 "
                  "Safari/537.36"}

# reading in data file from previous scraping
data_file = pd.read_csv(r'data.csv')


def get_soup(url):
    """
    Retrieve and parse the HTML content of a web page

    :param url: the URL of the page we want to scrape
    :return: a BeautifulSoup object representing the parsed HTML content
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def advert_info(url, current_id):
    """
    Scrapes data from 3 locations on a single page. From the title, the 'table' of data and the 'specifications tab'

    :param url: base url of Exchange & Mart
    :param current_id: the active advert ID to be scraped
    :return: combined_dataframe: pandas dataframe which contains data from the title of the ad, the 'table' and the
             'specifications tab'
    """

    # dictionary of data scraped from the website and inputted as a parameter
    first_data = {'makes and models': None,
                  'Id value': current_id}

    full_table_data = []
    accepted_ids = []
    rejected_ids_for_spec = []
    specs_list = []
    accumulated_data = []
    specs = {}

    # the types of data available in the 'table' of data (for internal combustion engines only, currently...)
    types_of_data = ['Year', 'Engine size', 'Mileage', 'Fuel type', 'Transmission', 'Colour', 'Body type', 'Mpg']
    soup = get_soup(url)

    # locating and scraping the data for the make and model of the car
    make_and_model = soup.find('h2', class_='col-xs-9').find('span', class_='ttl')
    first_data['makes and models'] = make_and_model.get_text(strip=True)

    # locating the data from the 'specification tab'
    specification_tab = soup.find_all("div", class_="adSpecItem")

    # locating the data from the 'table' of data
    table_of_info = soup.find_all("div", class_="adDetsItem")

    # scraping the data from the 'specification tab' into a dictionary with respective keys and values
    for item in specification_tab:
        data = list(item.stripped_strings)
        key = data[0].strip(':')
        value = data[1]
        specs[key] = value

    if specs:
        specs_list.append(specs)
    else:
        # sometimes the 'specification tab' is not always present. In this case we ignore the advert
        print('no given specification tab', current_id)
        rejected_ids_for_spec.append(current_id)

    # scraping the data from the 'table' into a list
    list_of_table_data = []
    for info in table_of_info:
        data = info.text.strip()
        list_of_table_data.append(data)

    # for electric and hybrid cars the 'table' of data doesn't have a length of 8
    if len(list_of_table_data) == 8:
        accepted_ids.append(current_id)
        accumulated_data.append(list_of_table_data)
        full_table_data.append(accumulated_data[-1])
    else:
        # in this case we ignore the advert and record the id for future use
        print('not all data present', list_of_table_data, 'rejected id value', current_id)
        return

    # turning the dictionaries and lists into dataframes for future manipulation
    specification_tab_dataframe = pd.DataFrame(specs_list)
    table_data_dataframe = pd.DataFrame(full_table_data)
    table_data_dataframe.columns = types_of_data

    # the 'specification tab' contains data we aren't interested in, so this only selects what is needed
    wanted_columns = ['Year', 'Engine size', 'Mileage',
                      'Fuel type', 'Transmission', 'Colour', 'Body type', 'Mpg',
                      'Wheel drive', 'Doors', 'Seats', 'Engine power', 'Top speed',
                      'Acceleration (0-62 mph)', 'CO2 rating', 'Tank range']
    specification_tab_dataframe = specification_tab_dataframe.filter(items=wanted_columns)
    make_and_model_and_id_df = pd.DataFrame(first_data, index=[0])

    # if any not applicable entries are present we ignore the advert
    for index, row in specification_tab_dataframe.iterrows():
        if row.isna().any():
            print('full spec data is not present')
            return

    # concatenate all 3 dataframes into 1
    combined_dataframe = pd.concat([make_and_model_and_id_df, table_data_dataframe, specification_tab_dataframe],
                                   axis=1, ignore_index=True)

    # final check that the combined_dataframe is of the correct dimension and then naming the columns
    if combined_dataframe.shape[1] == 18:
        combined_dataframe.columns = ['Make and model', 'ID value', 'Year', 'Engine size (litres)', 'Mileage (miles)',
                                      'Fuel type', 'Transmission', 'Colour', 'Body type', 'Mpg',
                                      'Wheel drive', 'Doors', 'Seats', 'Engine power (bhp)', 'Top speed (mph)',
                                      'Acceleration (0-62 mph) (seconds)', 'CO2 rating (g/km)', 'Tank range (miles)']

        # the scraped data sometimes has units. This removes all the units where necessary
        combined_dataframe['Engine size (litres)'] = combined_dataframe['Engine size (litres)'].str.slice(stop=-1)
        combined_dataframe['Mileage (miles)'] = combined_dataframe['Mileage (miles)'].str.slice(stop=-5)
        combined_dataframe['Mpg'] = combined_dataframe['Mpg'].str.slice(stop=-3)
        combined_dataframe['Engine power (bhp)'] = combined_dataframe['Engine power (bhp)'].str.slice(stop=-3)
        combined_dataframe['Top speed (mph)'] = combined_dataframe['Top speed (mph)'].str.slice(stop=-3)
        combined_dataframe['Acceleration (0-62 mph) (seconds)'] = combined_dataframe['Acceleration (0-62 mph) (seconds)'].str.slice(stop=-7)
        combined_dataframe['CO2 rating (g/km)'] = combined_dataframe['CO2 rating (g/km)'].str.slice(stop=-4)
        combined_dataframe['Tank range (miles)'] = combined_dataframe['Tank range (miles)'].str.slice(stop=-5)

        return combined_dataframe


def main():
    still_searching = True  # boolean: when false the task is complete and the scraper will stop

    # the consecutive amount of blank results we can get before considering all future adverts are blank/not created yet
    max_consecutive_inactive_ids = 50  # this number can be changed depending on how strict we are
    current_consecutive_inactive_ids = 0
    base_url = 'https://www.exchangeandmart.co.uk/ad/'

    # finding what id number the scraper got up to last time and then adding 1 and continuing from there
    current_id_number = data_file.iat[len(data_file['ID value']) - 1, data_file.columns.get_loc('ID value')] + 1
    updated_data = data_file

    while still_searching:
        if current_consecutive_inactive_ids > max_consecutive_inactive_ids:
            # terminate the scraping and output a csv file when we get to the limit of inactive ids
            updated_data.to_csv('data.csv', index=False, encoding='utf-8')
            still_searching = False
        else:
            # if we are not at the limit of inactive ids we search if the page exists. If it exists we run the scraper.
            # And then append the data to the 'master' dataframe
            soup = get_soup(base_url + str(current_id_number))
            if soup.find("div", id="vehicle-desc"):
                current_consecutive_inactive_ids = 0
                print(advert_info(base_url + str(current_id_number), current_id_number), current_id_number)
                updated_data = pd.concat([updated_data, advert_info(base_url + str(current_id_number),
                                                                    current_id_number)], axis=0, ignore_index=True)
                # move on to next id number
                current_id_number += 1
            else:
                # if the page doesn't exist. Increment the inactive id count and move onto next id number
                current_consecutive_inactive_ids += 1
                current_id_number += 1


if __name__ == "__main__":
    main()