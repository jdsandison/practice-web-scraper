import requests
from bs4 import BeautifulSoup
import csv

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

def find_ids(search_url):
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    div_elements = soup.find_all("div", class_="result-item")
    for div in div_elements:
        adid_values = [div["adid"]]

    return  adid_values



def find_listings(search_url):
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    parent_div = soup.find("div", adid="30186438")
    car_titles = parent_div.find("div", class_="result-item__description hidden-xs")
    for title in car_titles:
        car_title = title.text.strip()
        print(car_title)

def main():
    search_url = 'https://www.exchangeandmart.co.uk/used-cars-for-sale'
    #find_listings(search_url)
    find_ids(search_url)
    

if __name__ == "__main__":
    main()