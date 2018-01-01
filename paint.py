#!/usr/bin/env py
import time

import requests

from colorama import Fore, Back, Style, init

init()

col_dic = {
    (0, 0, 0): 0,
    (255, 255, 255): 1,
    (170, 170, 170): 2,
    (85, 85, 85): 3,
    (254, 211, 199): 4,
    (255, 196, 206): 5,
    (250, 172, 142): 6,
    (255, 139, 131): 7,
    (244, 67, 54): 8,
    (233, 30, 99): 9,
    (226, 102, 158): 10,
    (156, 39, 176): 11,
    (103, 58, 183): 12,
    (63, 81, 181): 13,
    (0, 70, 112): 14,
    (5, 113, 151): 15,
    (33, 150, 243): 16,
    (0, 188, 212): 17,
    (59, 229, 219): 18,
    (151, 253, 220): 19,
    (22, 115, 0): 20,
    (55, 169, 60): 21,
    (137, 230, 66): 22,
    (215, 255, 7): 23,
    (255, 246, 209): 24,
    (248, 203, 140): 25,
    (255, 235, 59): 26,
    (255, 193, 7): 27,
    (255, 152, 0): 28,
    (255, 87, 34): 29,
    (184, 63, 39): 30,
    (121, 85, 72): 31
}

col_lst = [
    (0, 0, 0),
    (255, 255, 255),
    (170, 170, 170),
    (85, 85, 85),
    (254, 211, 199),
    (255, 196, 206),
    (250, 172, 142),
    (255, 139, 131),
    (244, 67, 54),
    (233, 30, 99),
    (226, 102, 158),
    (156, 39, 176),
    (103, 58, 183),
    (63, 81, 181),
    (0, 70, 112),
    (5, 113, 151),
    (33, 150, 243),
    (0, 188, 212),
    (59, 229, 219),
    (151, 253, 220),
    (22, 115, 0),
    (55, 169, 60),
    (137, 230, 66),
    (215, 255, 7),
    (255, 246, 209),
    (248, 203, 140),
    (255, 235, 59),
    (255, 193, 7),
    (255, 152, 0),
    (255, 87, 34),
    (184, 63, 39),
    (121, 85, 72)
]


class user:

    def __init__(self, cookie_dict, last_time):
        self.cookie_dict = cookie_dict
        self.last_time = last_time


class task:
    def __init__(self, x, y, col):
        self.x = x
        self.y = y
        self.col = col


data = {'x': 0, 'y': 0, 'color': 0}
user_lst = []
task_que = []


def print_line():
    print(Fore.MAGENTA + "==============================================================================")


times = 0
mlst = []


def check_task(point):
    global times
    global mlst
    if times == 20:
        times -= 20
    if times == 0:
        try:
            q = requests.get("https://www.luogu.org/paintBoard/Board",
                             cookies=user_lst[0].cookie_dict)
        except:
            time.sleep(0.01)
            q = requests.get("https://www.luogu.org/paintBoard/Board",
                             cookies=user_lst[0].cookie_dict)
        mlst = q.text.split('\n')
    times += 1
    if mlst[point.x][point.y] == point.col:
        return True
    else:
        return False


with open("cookies.txt", "r") as cok:
    coks = cok.readlines()
    for i in coks:
        umid = i.split(' ')[0]
        clid = i.split(' ')[1]
        clid = clid.replace('\n', '')
        user_lst.append(
            user(dict(UM_distinctid=umid, __client_id=clid), time.time() - 29))
    print_line()
    print(Fore.CYAN + "Users:")
    for i in user_lst:
        print(Fore.YELLOW + "cookies: {0}".format(i.cookie_dict))
    print_line()
base_x = 624
base_y = 186
with open("base32.txt", "r") as pic:
    s = pic.readline()
    l = int(str(s).split(' ')[0])
    h = int(str(s).split(' ')[1])
    task_num = l * h
    lst = pic.readlines()
    for i in range(0, len(lst)):
        lst[i] = lst[i].replace('\n', '')
        for j in range(0, len(lst[i])):
            task_que.append(task(j + base_x, i + base_y, lst[i][j]))
    print(Fore.GREEN + "length: {0} height: {1}".format(l, h))
    print(Fore.GREEN + "{0} tasks added".format(l * h))
    print_line()

task_success = 0
task_success_que = []
log_timer = time.time()
while len(task_que) > 0:
    now_task = task_que[0]
    task_que.pop(0)
    stat = check_task(now_task)
    if stat == False:
        data['x'] = now_task.x
        data['y'] = now_task.y
        data['color'] = int(str(now_task.col), base=32)
        user = user_lst[0]
        user_lst.pop(0)
        if 30 + user.last_time > time.time():
            time.sleep(30 + user.last_time - time.time())
        try:
            r = requests.post("https://www.luogu.org/paintBoard/paint",
                              data=data, cookies=user.cookie_dict)
        except:
            time.sleep(0.01)
            r = requests.post("https://www.luogu.org/paintBoard/paint",
                              data=data, cookies=user.cookie_dict)
        if str(r.text).find("500") != -1:
            out = Fore.RED
            print(out + "Paint failed")
        else:
            out = Fore.GREEN
            print(out + "Paint succeed")
            task_success += 1
            task_success_que.append(time.time())
            if len(task_success_que) != 0:
                if time.time() - task_success_que[0] > 30:
                    task_success_que.pop(0)
        print(out + "ret_code: {0} text: {1}".format(
            r.status_code, r.text))
        print(out + "user: {0}".format(user.cookie_dict))
        print(Fore.CYAN + "pos&color: {0}".format(data))
        print_line()
        user.last_time = time.time() + 1
        user_lst.append(user)
    task_que.append(now_task)
    if time.time() - log_timer > 5:
        with open("stat.log", "w") as logger:
            logger.write("30s {0}\n".format(len(task_success_que)))
            logger.write("all {0}\n".format(task_success))
            logger.write("{0}\n".format(task_success / task_num))
        log_timer = time.time()
print("==============FINISHED=================")
print_line()
