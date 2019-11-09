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
    press = None
    name = '연합뉴스'
    url_base = 'https://www.yna.co.kr'

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

        for idx in range(10, 0, -1):
            urls.append("{}/news/{}".format(self.url_base, idx))

        for url in urls:
            try:
                _response = requests.get(url, headers=self.headers)
                # _response.encoding = self.press.encoding()
                _response.close()

            except requests.exceptions.ConnectionError as e:
                _second = random.randrange(5 * 60, 15 * 60)
                # sleep_with_message(_second, '리스트가 읽히지 않습니다. 차단을 피하기 위해서 긴 대기 시간을 가집니다.')
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

                # FIXME: 처음은 대부분 연합뉴스를 등록할 것을 예상합니다.
                press = ThePress.objects.first()
                if not Article.create_new(press=press, url=url, title=title, datetime=datetime_obj):
                    return False

                print(f'연합뉴스: {datetime_obj}: {title}: {url}')
                # Article.perceive('https://' + url, title, datetime_obj)

            time.sleep(10)
