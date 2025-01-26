import requests
from bs4 import BeautifulSoup
import json
def lhg():
    with open('Bot_token.json', 'r', encoding='utf-8') as f:
        return json.load(f)
def load_json():
    with open('register.json', 'r', encoding='utf-8') as f:
        return json.load(f)
def upload_json(users):
    with open('register.json', 'w', encoding='utf-8') as f:
        return json.dump(users, f)

def login_user(user_attempt, code, username):
    session = requests.Session()
    home_page = session.get("https://robocontest.uz")
    soup = BeautifulSoup(home_page.text, "html.parser")
    p = lhg()
    csrf_token = soup.find("meta", {"name": "csrf-token"})["content"]
    login_data = {
        "_token": csrf_token,
        "email": p['username'],
        "password": p['password'],
        "redirect": ""
    }
    login_response = session.post("https://robocontest.uz/login", data=login_data)
    try:
        another_page = session.get("https://robocontest.uz/attempts/" + str(user_attempt))

        soup = BeautifulSoup(another_page.text, "html.parser")
        textarea = soup.find("textarea", {"id": "code"})
        user_link = soup.find_all('a')
        user = user_link[19]['href']
        # print(user)
        # for i in user_link:
        #     if 'https://robocontest.uz/profile/' in i:
        #         user = i
        #         break
        # print(textarea.text.strip())
        # print(user)
        if code.strip() == textarea.text.strip() and username.strip() == user[user.rfind('/') + 1:].strip():
            return True
        return False
    except:
        with open('index4.html', 'w', encoding='utf-8') as f:
            f.write(another_page.text)
        print('Buyer, except')
        return False
    
def registerr(username, password):
    userss = load_json()
    k = userss[0]
    if username not in k:
        k[username] = password
        upload_json(userss)
        return True
    else:
        return False

def sign_up(username, password):
    users = load_json()[0]
    return users[username] == password