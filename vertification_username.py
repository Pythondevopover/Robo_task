import requests

def validation_username(username):
    user = 'https://robocontest.uz/profile/' + username
    re = requests.get(user)
    if re.status_code == 200:
        return True
    return False