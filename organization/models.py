from urllib.parse import urlparse

from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.db import models


class ThePress(models.Model):
    title = models.CharField('언론사 이름', max_length=128)
    main_url = models.URLField('대표 홈페이지', unique=True)
    mobile_url = models.URLField('모바일 홈페이지', unique=True)
    encoding = models.CharField('페이지 인코딩', max_length=8, default='UTF-8', choices=(
        ('UTF-8', 'UTF-8'),
        ('euc-kr', 'euc-kr'),
    ))
    user_agent = models.CharField('UserAgent', max_length=128)

    def __str__(self):
        return self.title

    @classmethod
    def find_by_title(cls, title):
        return cls.objects.filter(title=title).first()


class PressMixin(object):
    name = ''
    url_base = ''

    body = ''
    soup_body = None
    soup_list = None
    soup_section = None

    class Meta:
        abstract = True

    def is_same_domain(self, target):
        base_parsed = urlparse(self.url)
        target_parsed = urlparse(target)

        base = base_parsed.netloc.split('.')[0]

        for s in target_parsed.netloc.split('.'):
            if base == s:
                return True

        return False

    def list_soup(self, body):
        self.body = body
        self.soup_body = BeautifulSoup(self.body, 'lxml')
        self.soup_list = self.soup_body.select_one(self.selector_list)

        return self.soup_list

    def list_section(self, soup_list=None):
        if soup_list is not None:
            self.list_soup = soup_list

    """
    @classmethod
    def get_object(cls):
        try:
            return cls.objects.get(title=cls.name)
        except ObjectDoesNotExist:
            return None

    def articles_to_fill_in(self):
        # TODO: 뭔가 분명히 더 좋은 방법이 있을 듯 싶은데 ...
        article_class = None
        article_class_all = [ArticleYonhap, ArticleChosun, ArticleDonga, ArticleHani, ArticleHankyung,
                             ArticleKhan, ArticleMk, ArticleMunhwa]

        for a_c in article_class_all:
            if isinstance(self, a_c.press_class):
                article_class = a_c

        if article_class is None:
            raise Exception('아직 생성되지 않은 언론사 기사 형태 입니다')

        return article_class.list_to_fill()
    """


class PressYonhap(PressMixin, ThePress):
    name = '연합뉴스'
    url_base = 'https://www.yna.co.kr'

    selector_list = '.headline-list ul'

    class Meta:
        proxy = True

    name = '연합뉴스'
    url_base = 'https://www.yna.co.kr'

    selector_list = '.headline-list ul'

    @property
    def link_url(self):
        return self.url + '?section=news'

    def fill_article_head(self, soup_article):
        if soup_article is None:
            return

        self.soup_article = soup_article

        title = self.soup_article.select_one('h1').string
        soup_article_content = self.soup_article.select_one('.article')

        if title is None:
            self.title = ''
        elif title.strip() != '':
            self.title = title

        if soup_article_content is None:
            soup_article_content = ''

        self.soup_article_content = soup_article_content

        # _send_datetime = self.soup_article.select_one('.share-info').find('em').string
        # _image = _content.select_one('.article-img')

        # FIXME: 서브 타이틀이 없는 경우도 있음
        # # 아마도 부제목 같은 느낌인 듯
        # for string in _content.select_one('.stit').stripped_strings:
        #     pass
        #     # print(repr(string))
        # _content.select_one('.stit').decompose()

        # TODO: 기사에 이미지를 찾아서 넣어주자




class Reporter(models.Model):
    def __str__(self):
        candidate = self.reporterdetail_set
        if candidate.exists():
            return str(candidate.last())

        return '미지정'


class ReporterDetail(models.Model):
    reporter = models.ForeignKey('Reporter', default=None, blank=True, on_delete=models.CASCADE)
    press = models.ForeignKey('ThePress', on_delete=models.CASCADE)
    name = models.CharField('이름', max_length=32, default='', blank=True)
    email = models.EmailField('이메일', default=None, blank=True)
    # 기자 공개 이미지 URL

    def __str__(self):
        return f"{self.press}: {self.name}[{self.email}]"

    def save(self, *args, **kwargs):
        # FIXME: 이렇게 하는게 맞으려나?
        if self.reporter_id is None:
            self.reporter = Reporter.objects.create()

        super().save(*args, **kwargs)

    def validate_unique(self, exclude=None):
        if self.email:
            if ReporterDetail.objects.filter(email=self.email).exists():
                error = {'email': ValidationError('이메일이 중복되었습니다.')}
                raise ValidationError(error)


class ArticleReporter(models.Model):
    article = models.ForeignKey('news.Article', on_delete=models.CASCADE)
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
