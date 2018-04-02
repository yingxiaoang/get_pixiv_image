import requests
from bs4 import BeautifulSoup

# 获得post_key以便在登录时使用
def get_post_key():
    url = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.find('input')['value']


def lodin_pixiv(pixiv_id,password):
    headers = {}
    url = "https://accounts.pixiv.net/api/login?lang=zh"
    data = {"pixiv_id": pixiv_id,
            "password": password}
    data['post_key'] = get_post_key()
    r = requests.post(url=url,data=data)
    # 通过登录返回的headers中的Set-Cookie设置Cookie
    cookie = r.headers['Set-Cookie'] 
    headers["Referer"] = "https://www.pixiv.net"
    headers["Cookie"] = cookie
    headers["user-agent"]="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    # 返回 hraders在以后的爬虫中使用 如果 r.status_code不等于200表示模拟登录出错
    return hraders, r.status_code











