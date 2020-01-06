import random
import time
from datetime import datetime, timedelta

import pytz
import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from django.utils import timezone

from news.models import Article
from organization.models import ThePress


class Command(BaseCommand):
    help = '국민일보 최신기사 리스트를 DB에 추가한다'
    name = '국민일보'
    press = ThePress.find_by_title(title=name)
    url_base = 'https://kmib.co.kr'

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

        for adate in dates:
            for page in range(10, 0, -1):
                url = f'http://news.kmib.co.kr/article/list.asp?sid1=all&sid2=&page={page}&sdate={adate:%Y%m%d}&st='
                urls.append(url)

        for url in urls:
            try:
                _header = {
                    'User-Agent': self.press.user_agent
                }
                _response = requests.get(url, headers=_header)
                _response.encoding = self.press.encoding
                _response.close()

            except requests.exceptions.ConnectionError as e:
                _second = random.randrange(5 * 60, 15 * 60)
                time.sleep(_second)
                exit()

            soup = BeautifulSoup(_response.text, 'lxml')
            soup_list = soup.select_one('.nws_list')

            for item in soup_list.select('div.nws'):
                dt = item.select_one('dt').select_one('a')
                url = dt['href']
                title = dt.string
                datetime_str = item.select_one('dd.date').string
                datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
                datetime_obj = timezone.make_aware(datetime_obj, timezone=pytz.timezone('Asia/Seoul'), is_dst=False)
                summary = item.select_one('dd.tx').string.strip()
                thumbnail_obj = item.select_one('p.pic a img')
                if thumbnail_obj:
                    thumbnail_src = thumbnail_obj['src']

                if Article.create_new(press=self.press, url=url, title=title, datetime=datetime_obj) is None:
                    time.sleep(10)
                    continue

                print(f'국민일보: {datetime_obj}: {title}: {url}')

            time.sleep(10)
