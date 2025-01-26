import requests
from bs4 import BeautifulSoup
def search_picture_img(username):
    url = f'https://robocontest.uz/profile/{username}'
    re = requests.get(url)
    if re.status_code == 200:
        so = BeautifulSoup(re.text, 'html.parser')
        sr = so.find('img')
        return sr['src']
    elif re.status_code == 404:
        return 'Siz username ni xato kiritdingiz!!!'
    else:
        return 'Saytda texnik ishlar bolayapti.'