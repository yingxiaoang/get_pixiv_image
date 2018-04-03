import requests
from bs4 import BeautifulSoup
import os
import re
from multiprocessing import Process
import time


headers = {"Referer": "https://www.pixiv.net",
           'Cookie': "Cookie" # 复制Cookie进来
           }
main_url = 'https://www.pixiv.net'
init = "https://www.pixiv.net/member_illust.php?id="
page_ = 'https://www.pixiv.net/member_illust.php'
p = re.compile(r'mode=medium')


def run(pid):
    if pid=='':
        return 0
    pages = []
    page_url = init + pid
    pages.append(page_url)
    r = requests.get(url=page_url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')


    try:
        menu = soup.select('.column-order-menu')[0].find_all('a')
        for i in menu:
            pages.append(page_ + i.get('href'))
        pages.pop()
    except:
        pass
    for i in pages:
        r = requests.get(url=i, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        imgs = soup.select('._image-items')[0].find_all("a")
        for i in imgs:
            img_class = i.get('class')
            if img_class is not None:
                if len(img_class)>= 4:
                    img_url =  p.sub(repl='mode=manga', string=i.get('href'), count=1)
                    r = requests.get(url = main_url + img_url,headers = headers)
                    soup = BeautifulSoup(r.text,'lxml')
                    img = soup.select('.item-container')
                    for i in img:
                        r = requests.get(main_url +i.a.get('href'),headers = headers)
                        soup = BeautifulSoup(r.text,'lxml')
                        r = requests.get(soup.img.get('src'), headers = headers)
                        image = open('image/' + os.path.basename(soup.img.get('src')), 'wb')
                        image.write(r.content)
                        image.close()
                        print(os.path.basename(soup.img.get('src'))+'下载成功')
                        time.sleep(0.5)
                else:
                    img_url = main_url+i.get('href')
                    r = requests.get(url=img_url,headers = headers)
                    soup = BeautifulSoup(r.text,'lxml')
                    for i in soup.select('.wrapper'):
                        if i.img is not None:
                            img = i.img.get('data-src')
                            r = requests.get(url=img,headers = headers)
                            image = open('image/'+ os.path.basename(img),'wb')
                            image.write(r.content)
                            image.close()
                            print(os.path.basename(img)+'下载成功')
                            time.sleep(0.5)



if __name__ == '__main__':
    while True:
        print("请输入作者ID：")
        pid = input()
        if pid == 'quit':
            quit()
        run1 = Process(target=run, args=(pid,))

        #print("请输入作者ID：")
        #pid = input()
        #if pid == 'quit':
        #    quit()
        #run2 = Process(target=run, args=(pid,))
        run1.run()
        #run2.run()
