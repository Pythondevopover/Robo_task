import requests
from bs4 import BeautifulSoup

def user_about(username: str) -> list:
    url = f'https://robocontest.uz/profile/{username}'
    re = requests.get(url)
    if re.status_code == 200:
        so = BeautifulSoup(re.text, 'html.parser')
        rating_name = so.find('h4', class_='text-center m-0 font-weight-bold').text
        div = so.find('div', class_='row mt-3').text.strip().split()
        robo_rating_max = div[-3]
        robo_rating = div[-5]
        robo_rank = div[0]
        if robo_rating_max == '~1500':
            return [robo_rank, 1500, 1500, 'Pupil']
        return [robo_rank, robo_rating, robo_rating_max[0:-1], rating_name]
    elif re.status_code == 404:
        return ['Username xato kiritilgan!!!']
    else:
        return ['Saytda texnik ishlar bolayapti!!!']