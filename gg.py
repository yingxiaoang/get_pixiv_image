import requests
from bs4 import BeautifulSoup


"""




headers["Referer"] = "https://www.pixiv.net"
headers['Cookie'] = "PHPSESSID=19604805_809aab162b6781faa8a883d0d8241163;"

mode = 'daily'

date = 20180215

url = "https://www.pixiv.net/ranking.php?mode={0}&date={1}".format(mode, date)


r = requests.get(url, headers = headers)
p = re.compile('ranking-items-container')

print(p.sub("www.baidu.com", r.text))
"""

headers = {}

def get_post_key():
    url = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.find('input')['value']


url = "https://accounts.pixiv.net/api/login?lang=zh"

data = {"pixiv_id": "账号",
        "password": "密码"}
data['post_key'] = get_post_key()

r = requests.post(url=url,data=data)
cookie = r.headers['Set-Cookie']
headers["Referer"] = "https://www.pixiv.net"
headers['Cookie'] = cookie




