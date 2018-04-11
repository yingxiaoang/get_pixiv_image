import requests
from bs4 import BeautifulSoup
import json
import os
import time
import login

headers = dict()
headers["Referer"] = "https://www.pixiv.net"
headers['Cookie'] , status_code = login.lodin_pixiv(pixiv_id, password)
mode = ['daily', 'daily_r18', 'weekly', "weekly_r18", 'monthly']
content = ['', '&content=illust', '&content=manga']


# 生存还是毁灭,这是一个问题
def shakespeare(tags, titles, id):
    is_exis = True
    if os.path.exists('image'):
        with open('image.txt', 'r') as f:
            for i in f:
                if i[:-1] == str(id):
                    return False
    for i in tags:
        if title == i or len(titles) == 0:
            return is_exis
    return False


def is_double(count): # 判断是否多图
    if count > 1:
        return True
    return False


def set_url(date, mode, content):
    if len(date) != 0:
        main_url = 'https://www.pixiv.net/ranking.php?mode={0}&date={1}'.format(mode, date)
    else:
        main_url = 'https://www.pixiv.net/ranking.php?mode={0}'.format(mode)
    ref = "&rn-h-all-3"
    tt = '&baf01eb9218770f948d6e87c9eb71fe9'
    main_url += ref
    main_url += "&format=json"
    main_url += tt
    main_url += content
    return main_url


def get_image_list(url, titles):
    image_list = []
    page = 2
    for p in range(1, page):
        url += '&p={0}'.format(p)
        r = requests.get(url, headers=headers)
        data = json.loads(r.text)
        for i in data['contents']:
            down = shakespeare(i['tags'], titles,  i['illust_id'])
            if down:
                f = open('image.txt', 'a')
                f.write(str(i['illust_id']))
                f.write('\n')
                is_doubles = is_double(int(i['illust_page_count']))
                if int(i['illust_type']) != 2:
                    image_list.append([is_doubles, i['illust_id']])
    return image_list





def save(img):
    if os.path.exists('image'):
        pass
    else:
        os.makedirs('image')
    r = requests.get(url=img, headers=headers)
    try:
        image = open('image/' + os.path.basename(img), 'xb')
        image.write(r.content)
        image.close()
        print(os.path.basename(img) + '下载成功')
    except FileExistsError:
        pass
    time.sleep(0.5)


def down_load_one(image_id):
    image_ual = 'https://www.pixiv.net/member_illust.php?mode=manga_big&illust_id={0}&page=0'.format(image_id)
    r = requests.get(image_ual, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    img = soup.img.get('src')
    return img


def down_load(image_list):
    if len(image_list) == 0:
        return None
    for i in image_list:
        if i[0]:
            img_url = down_load_one(i[1])
        else:
            image_ual = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id={0}'.format(i[1])
            r = requests.get(image_ual,headers = headers)
            soup = BeautifulSoup(r.text, 'lxml')
            img = soup.select('.wrapper')
            for j in img:
                if j.img is not None:
                    img_url = j.img.get('data-src')
        save(img_url)




print("选择默认直接回车")
print("是否指定标签(默认不指定):")
title = input()
print("是否指定日期(默认最新):")
date = input()
print("是否指定排行榜类型(默认综合) 1插画 2漫画:")
content_ = input()
if len(content_) == 0:
    content_ = 0
else:
    content_ = int(content_)

print("是否指定排行榜(默认日榜) 1周榜 2月榜(出于和谐,不考虑R18的下载):")
mode_ = input()
if len(mode_) == 0:
    mode_ = 0
else:
    mode_ = int(mode_)



urls = set_url(date, mode[mode_], content[content_])
image_lists = get_image_list(urls, title)
down_load(image_lists)

