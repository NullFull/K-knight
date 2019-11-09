import random
from urllib.parse import urlparse
from datetime import datetime, timedelta

import pytz
import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from django.utils import timezone



class Command(BaseCommand):
    help = '국민일보 최신기사 리스트를 DB에 추가한다'
    press = None
    name = '국민일보'
    url_base = 'https://kmib.co.kr'

    headers = {'User-Agent': 'Mozilla/5.0 ' + '(Windows NT 10.0; Win64; x64) ' +
                             'AppleWebKit/537.36 (KHTML, like Gecko) ' + 'Chrome/60.0.3112.113 Safari/537.36'}

    # def add_arguments(self, parser):
    #     parser.add_argument('press_keyword', type=str)
    #

    def handle(self, *args, **options):
        """
        우선 연합 뉴스만 예시로 작성한다.
        """
        urls = list()

        now = datetime.now()
        dates = [now]
        if now.hour < 6:
            dates.append(now - timedelta(1)) # requirement: 6시간 이상 지나지 않았으면 전날도 크롤링

        print(dates)
        for adate in dates:
            for page in range(10, 0, -1):
                url = f'http://news.kmib.co.kr/article/list.asp?sid1=all&sid2=&page={page}&sdate={adate:%Y%m%d}&st='
                urls.append(url)
                print(url)

        for url in urls:
            try:
                _response = requests.get(url, headers=self.headers)
                _response.encoding = 'cp949'
                _response.close()

            except requests.exceptions.ConnectionError as e:
                _second = random.randrange(5 * 60, 15 * 60)
                # sleep_with_message(_second, '리스트가 읽히지 않습니다. 차단을 피하기 위해서 긴 대기 시간을 가집니다.')
                exit()

            soup = BeautifulSoup(_response.text, 'lxml')
            soup_list = soup.select_one('.nws_list')

            for item in soup_list.select('div.nws'):
                dt = item.select_one('dt').select_one('a')
                url = dt['href']
                title = dt.string
                datetime_str = item.select_one('dd.date').string
                datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
                summary = item.select_one('dd.tx').string.strip()
                thumbnail_obj = item.select_one('p.pic a img')
                if thumbnail_obj: thumbnail_src = thumbnail_obj['src']

                print(f'국민일보: {datetime_obj}: {title}: {url}')

