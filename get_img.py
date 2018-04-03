import requests
from bs4 import BeautifulSoup
import os
import re
from multiprocessing import Process
import time


headers = {"Referer": "https://www.pixiv.net",
           'Cookie': "p_ab_id=1; p_ab_id_2=2; _tdim=dea127b0-4cf4-4baf-c090-c38033ece874; _ga=GA1.2.1438554757.1517406172; PHPSESSID=19604805_ba9f5779c7c90368b79e9a1a12360c13; device_token=46bdeb548e18bd95b5010929b847baac; c_type=21; a_type=0; b_type=1; login_ever=yes; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=19604805=1^9=p_ab_id=1=1^10=p_ab_id_2=2=1^11=lang=zh=1; module_orders_mypage=%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22showcase%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; is_sensei_service_user=1; __utmz=235335808.1517749127.4.2.utmcsr=yuriimg.com|utmccn=(referral)|utmcmd=referral|utmcct=/artist/14609740.html; __utmc=235335808; __utma=235335808.1438554757.1517406172.1517749127.1517753540.5; __utmt=1; __utmb=235335808.1.10.1517753540; tag_view_ranking=BU9SQkS-zU~y8GNntYHsi~NpsIVvS-GF~8Qlpl5et8m~JfsJE364lQ~gooMLQqB9a~Pk8F1M8-ms~VutBLvJmQ-~Qa8ggRsDmW~J99Gky7rC1~di65ET2Nrn~w6_tFfU5NW~6-4NLtqCXd~TCnz1buGzH~5Bfbh4tay-~h93kaJn5ZV~1F9SMtTyiX~sWTiWi6Mgm~qzoSdFnKb5~7L0ZYtv-Sg~Kpkq9GJk9i~ETjPkL0e6r~TOMV4MjMlf~oYiO-UdYgy~Lt-oEicbBr~5FCQSxfgUm~bYfigtcm_W~WbBWp_OUQ1~S6OJ9uijaS~26-Sd3V3Py~d_xJYFN472~7b1_RhnP20~Iy5hBUIsn7~gtqKAgwYdi~sFB6DB7I46~L15a_eAeOe~QH8eoBQs4C~RUEOTAVNfI~u3cdrQqm4P~RFxnRuAN7K~ehP5NJ0cy5~EiyJCF78Zu~2_8O4KFO0M~pzzjRSV6ZO~RTJMXD26Ak; _td=1611301d-cebc-4338-90b8-30ac3cd21dd2"

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
