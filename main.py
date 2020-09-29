from urllib.request import urlopen
from bs4 import BeautifulSoup

import threading

maxPage = 1  # max : 101
server = 1  # 1: 세오 7:통합
last_no = 0
end = False


def get_soup(target_url):
    html = urlopen(target_url)
    return BeautifulSoup(html, 'html.parser')


def extract_data(soup):
    table = soup.find('div', {'class': 'bg_list'})
    rows = table.find_all('tr')

    for idx, row in enumerate(rows):
        if idx == 0:
            continue  # skip th

        column = row.find_all('td')
        no = column[0].get_text()
        title = column[1].get_text()
        username = column[2].get_text()
        datetime = column[3].get_text()
        global last_no

        if int(no) > int(last_no):
            last_no = no
            if '월영' in title or '쿠라눔' in title:
                print(title, username, datetime)


def execute_func(sec):
    for pageNo in range(1, maxPage + 1):
        target_url = "http://lod.nexon.com/community/game/list.asp?GotoPage={0}&SearchBoard=4&SearchCategory2={1}".format(
            pageNo, server)
        soup = get_soup(target_url)
        extract_data(soup)

        threading.Timer(sec, execute_func, [sec]).start()


execute_func(3)
