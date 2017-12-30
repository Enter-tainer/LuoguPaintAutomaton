#!/usr/bin/env python3
import time

import requests

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


def dis(c1, c2):
    return (c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2


def get_nearest(col):
    mindis = dis(col, col_lst[0])
    mincol = col_lst[0]
    for i in col_lst:
        if dis(i, col) < mindis:
            mindis = dis(i, col)
            mincol = i
    return mincol


data = {'x': 0, 'y': 0, 'color': 2}
user_lst = []
with open("cookies.txt", "r") as cok:
    coks = cok.readlines()
    for i in coks:
        umid = i.split(' ')[0]
        clid = i.split(' ')[1]
        clid = clid.replace('\n', '')
        user_lst.append(
            user(dict(UM_distinctid=umid, __client_id=clid), time.time() - 29))
    print("Users:")
    for i in user_lst:
        print("cookies: {0}\n".format(i.cookie_dict))


with open("ttt.ppm", "r") as pic:
    with open("test.ppm", "w") as out:
        pic.readline()
        pic.readline()
        s = pic.readline()
        pic.readline()
        l = int(str(s).split(' ')[0])
        h = int(str(s).split(' ')[1])
        print(l)
        print(h)
        out.write("P3\n{0} {1}\n255\n".format(l, h))
        base_x = 690
        base_y = 205
        for i in range(0, h):
            for j in range(0, l):
                r = int(pic.readline())
                g = int(pic.readline())
                b = int(pic.readline())
                bestcol = get_nearest((r, g, b))
                out.write("{0} {1} {2}\n".format(
                    bestcol[0], bestcol[1], bestcol[2]))
                bestnum = col_dic[bestcol]
                data['x'] = base_x + j
                data['y'] = base_y + i
                data['color'] = bestnum
                user = user_lst[0]
                user_lst.pop(0)
                if 30 + user.last_time > time.time():
                    time.sleep(30 + user.last_time - time.time())
                r = requests.post("https://www.luogu.org/paintBoard/paint",
                                  data=data, cookies=user.cookie_dict)
                print("ret_code: {0} text: {1}\n".format(
                    r.status_code, r.text))
                print("user: {0}\n".format(user.cookie_dict))
                print("pos&color: {0}\n".format(data))
                print("=======================================\n")
                user.last_time = time.time() + 1
                user_lst.append(user)

'''
rgb(0, 0, 0),
rgb(255, 255, 255),
rgb(170, 170, 170),
rgb(85, 85, 85),
rgb(254, 211, 199),
rgb(255, 196, 206),
rgb(250, 172, 142),
rgb(255, 139, 131),
rgb(244, 67, 54),
rgb(233, 30, 99),
rgb(226, 102, 158):,
rgb(156, 39, 176):,
rgb(103, 58, 183):,
rgb(63, 81, 181):,
rgb(0, 70, 112):,
rgb(5, 113, 151):,
rgb(33, 150, 243):,
rgb(0, 188, 212):,
rgb(59, 229, 219):,
rgb(151, 253, 220):,
rgb(22, 115, 0):,
rgb(55, 169, 60):,
rgb(137, 230, 66):,
rgb(215, 255, 7):,
rgb(255, 246, 209):,
rgb(248, 203, 140):,
rgb(255, 235, 59):,
rgb(255, 193, 7):,
rgb(255, 152, 0):,
rgb(255, 87, 34):,
rgb(184, 63, 39):,
rgb(121, 85, 72):
'''
