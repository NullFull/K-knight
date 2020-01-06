import datetime
import random
import time
from urllib.parse import urlparse

import pytz
import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from django.utils import timezone

from news.models import Article
from organization.models import ThePress


class Command(BaseCommand):
    help = '연합뉴스 최신기사 리스트를 DB에 추가한다'
    name = '연합뉴스'
    press = ThePress.find_by_title(title=name)
    url_base = 'https://www.yna.co.kr'

    # def add_arguments(self, parser):
    #     parser.add_argument('press_keyword', type=str)
    #
    def handle(self, *args, **options):
        """
        우선 연합 뉴스만 예시로 작성한다.
        """
        urls = list()

        for idx in range(10, 0, -1):
            urls.append("{}/news/{}".format(self.url_base, idx))

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

            soup_body = BeautifulSoup(_response.text, 'lxml')
            soup_list = soup_body.select_one('.headline-list ul')

            soup_section = soup_list.find_all('li', {'class': 'section02'})

            for item in reversed(soup_section):
                title = item.select_one('.news-tl').select_one('a').string
                url_orig = item.select_one('.news-tl').select_one('a')['href']
                url_parsed = urlparse(url_orig)
                url = url_parsed.netloc + url_parsed.path

                datetime_string = item.select_one('.lead').select_one('.p-time').string
                datetime_obj = datetime.datetime.strptime(datetime_string, '%m-%d %H:%M').replace(year=2019)
                datetime_obj = timezone.make_aware(datetime_obj, timezone=pytz.timezone('Asia/Seoul'), is_dst=False)

                if not Article.create_new(press=self.press, url=url, title=title, datetime=datetime_obj):
                    return False

                print(f'연합뉴스: {datetime_obj}: {title}: {url}')
                # Article.perceive('https://' + url, title, datetime_obj)

            time.sleep(10)
