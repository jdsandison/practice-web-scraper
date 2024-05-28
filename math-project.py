import math
import requests
from bs4 import BeautifulSoup
import random


def test():
    postcode = 'DN1 1AQ'
    lat_long = (53.52109, -1.13916)

    # to go 10 miles due north from DN1 1AQ:
    new_lat = lat_long[0] + 10/69  # 69 miles per degree latitude

    # to go 10 miles due east from DN1 1AQ:
    new_long = lat_long[1] + 10/(math.cos(math.radians(lat_long[0])) * 69)

    print('10 miles north: ', new_lat, '10 miles east: ', new_long)


def test():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 '
        'Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 '
        'Safari/537.36 Edge/18.18362', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Mobile '
                                       'Safari/537.36', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS '
                                                        'X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                                                        'Version/14.0.2 Mobile/15E148 Safari/604.1']

    url = ''
    user_agent = random.choice(user_agents)
    headers = {
        "User-Agent": user_agent}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    html = soup.prettify()


    response2 = requests.get(url, user_agent)
    print(response2)


def main():
    test()


if __name__ == '__main__':
    main()