import requests
from bs4 import BeautifulSoup
from random import randint, shuffle
from tasks_diff import f

def version_1_1_choice_task(username: str, diff_mn: int, diff_mx: int) -> list:
    url = f'https://robocontest.uz/profile/{username}/tasks'
    task_url = f'https://robocontest.uz/tasks/'

    if requests.get(url).status_code == 200:
        mp = f()
        ans = []
        for i in range(1, 1213):
            if diff_mn <= mp[str(i)] <= diff_mx:
                ans.append((i, mp[str(i)]))
        shuffle(ans)
        answer_task = -1
        answer_diff = -1
        for task,diff in ans:
            t = True
            for i in range(1,61):
                nw_url = url + '?page=' + str(i)
                response = requests.get(nw_url)

                soup = BeautifulSoup(response.text, 'html.parser')

                div = soup.find('div', class_='table-responsive')

                ans = div.text.strip()
                if str(task).zfill(4) in ans:
                    t = False
                    break
            if t:
                answer_task = task
                answer_diff = diff
                break
        if answer_diff == answer_task == -1:
            return [f'Siz [{diff_mn};{diff_mx}] oraliqdagi barcha masalalrni ishlagansiz!!!']

        return [answer_diff, task_url + str(answer_task).zfill(4), answer_task]
    elif requests.get(url).status_code == 404:
        return ['Siz usernameingizni xato kitdingiz!!!']
    else:
        return ['Saytda qandaydir texnik ishlar bolayapti!!!']

def choice_task(username, dificult_mn, dificult_mx):
    url = f'https://robocontest.uz/profile/{username}/tasks'
    task_url = f'https://robocontest.uz/tasks/'
    while True:
        p = randint(1,1212)
        nw_task_url = task_url + str(p).zfill(4)
        re = requests.get(nw_task_url)

        so = BeautifulSoup(re.text, 'html.parser')

        di = so.find('div', class_='px-3 pt-3')

        res = di.text.strip()[38:45].strip()
        res = res[0:(res.find('%') - 1)]
        if not(dificult_mn <= int(res) <= dificult_mx):
            continue
        t = True
        for i in range(1,100):
            nw_url = url + '?page=' + str(i)
            response = requests.get(nw_url)

            soup = BeautifulSoup(response.text, 'html.parser')

            div = soup.find('div', class_='table-responsive')

            ans = div.text.strip()
            if str(p).zfill(4) in ans:
                t = False
                break
        if t:
            break
    ans = [res, 'https://robocontest.uz/tasks/' + str(p).zfill(4)]
    # print(ans)
    return ans

def difficult(diff):
    if 1 < diff <= 10:
        return 3
    if diff <= 25:
        return 8
    if diff <= 35:
        return 17
    if diff <= 50:
        return 30
    if diff <= 70:
        return 45
    if diff <= 85:
        return 60
    return 120

def accmi(task_number, username):
    for i in range(1, 62):
        url = f'https://robocontest.uz/profile/{username}/tasks?page=' + str(i)
        re = requests.get(url)

        so = BeautifulSoup(re.text, 'html.parser')

        div = so.find('div', class_='table-responsive')

        ans = div.text.strip()
        if str(task_number).zfill(4) in ans:
            return True
    return False



# print(choice_task('python_devopover', 30, 1))