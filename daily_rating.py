from datetime import *
import requests
from bs4 import BeautifulSoup
import json

def load_rank():
    with open('rank.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def upload_rank(ranks):
    with open('rank.json', 'w', encoding='utf-8') as f:
        return json.dump(ranks, f)

def rating(username):
    ranks = load_rank()
    rankss = ranks[0]
    td = str(datetime.today())[0:10]
    year, month, day = td.split('-')
    ty = f'{day}.{month}.{year}'
    try:
        if username in rankss[ty][0]:
            rankss[ty][0][username] += 1
        else:
            rankss[ty][0][username] = 1
    except:
        rankss[ty] = [{}]
        rankss[ty][0][username] = 1
    upload_rank(ranks)

def daily_top_users():
    ranks = load_rank()[0]
    td = str(datetime.today())[0:10]
    year, month, day = td.split('-')
    ty = f'{day}.{month}.{year}'
    try:
        ranks = ranks[ty][0]
        if len(ranks) >= 10:
            ans = {}
            cnt = 0
            for i,j in dict(sorted(ranks.items(), key=lambda item: item[1], reverse=True)).items():
                if cnt != 9:
                    ans[i] = j
                    cnt += 1
                else:
                    break
            print(ans)
            return [ans]
        else:
            return [dict(sorted(ranks.items(), key=lambda item: item[1], reverse=True))]
    except:
        return [False]
        
def my_rating(username):
    ranks = load_rank()[0]
    td = str(datetime.today())[0:10]
    year, month, day = td.split('-')
    ty = f'{day}.{month}.{year}'
    try:
        return ranks[ty][0][username]
    except:
        return 0

# rating('python_devopover')
# td = str(datetime.today())[0:10]
# year, month, day = td.split('-')
# ty = f'{day}.{month}.{year}'
# ranks = load_rank()
# srr = dict(sorted(ranks[0][ty][0].items(), key=lambda item: item[1], reverse=True))
# print(srr)
# print(rating('python_devopover'))
# print(daily_top_users())
# print(my_rating('python_devopover'))
# k = load_rank()
# print(k)