from django.db import models
from django.utils import timezone


class Article(models.Model):
    press = models.ForeignKey('organization.ThePress', on_delete=models.CASCADE)
    # INFO: 별 의미 없는 기자 및 기사가 연결이 있을 수 있음 (편집부 등...)
    reporters = models.ManyToManyField('organization.Reporter', through='organization.ArticleReporter')
    url = models.URLField('절대 주소')
    # last = models.ForeignKey('ArticleContent', default=None, on_delete=models.SET_DEFAULT)
    deleted = models.BooleanField('삭제된 기사', default=False)

    com_result_title = models.ForeignKey(
        'analysis.MatchRule', default=None, null=True, blank=True, on_delete=models.SET_DEFAULT,
        related_name='com_result_title_rule_id')
    com_result_content = models.ForeignKey(
        'analysis.MatchRule', default=None, null=True, blank=True, on_delete=models.SET_DEFAULT,
        related_name='com_result_content_rule_id')
    human_result_title = models.BooleanField('제목 사람 판단 결과', default=False)
    human_result_content = models.BooleanField('내용 사람 판단 결과', default=False)

    perceived_at = models.DateTimeField('시스템에서 인지한 시간', default=timezone.now)
    created_at = models.DateTimeField('기사 작성 시간', default=timezone.now)
    updated_at = models.DateTimeField('기사 업데이트 시간', default=None, blank=True, null=True)

    def __str__(self):
        candidate = self.articlecontent_set
        if candidate.exists():
            return str(candidate.last())

        return '본문 미 연결'


class ArticleContent(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    name = models.CharField('이름 판단 근거', max_length=128, default=None, blank=True, null=True)
    email = models.CharField('이메일 판단 근거', max_length=128, default=None, blank=True, null=True)
    title = models.CharField('제목', max_length=128, default=None, blank=True, null=True)
    content = models.TextField('내용', default=None, blank=True, null=True)
    perceived_at = models.DateTimeField('시스템에서 인지한 시간', default=timezone.now)
    created_at = models.DateTimeField('기사 작성 시간', default=timezone.now)
    updated_at = models.DateTimeField('기사 업데이트 시간', default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.article.press}: {self.title}"

    @classmethod
    def browser_agent(cls):
        return 'Mozilla/5.0 ' + '(Windows NT 10.0; Win64; x64) ' + \
               'AppleWebKit/537.36 (KHTML, like Gecko) ' + \
               'Chrome/60.0.3112.113 Safari/537.36'

    @classmethod
    def get_headers(cls):
        headers = {'User-Agent': cls.browser_agent()}
        return headers

    @classmethod
    def encoding(cls):
        return 'UTF-8'

    """
    
    
    @classmethod
    def perceive(cls, url, title, created):
        # TODO: 단순히 URL 만 넣는 경우도 고려하자!
        if cls.objects.filter(url=url).count():
            return None

        rule_ignore = ListIgnoreRule.match_all(title)
        if rule_ignore is not None:
            # print("[{}]: {}".format(title, rule_ignore.title))
            return None

        # TODO: 생성일을 정확하게 기입할 수 없는 경우 = 없는 경우
        instance = cls(url=url, title=title, created_at=created)
        instance.press = Press.find_from_url(url)

        try:
            instance.save()
            return instance

        except IntegrityError as e:
            print(e)
            return None

    @classmethod
    def list_to_fill(cls):
        # FIXME: 기사의 내용이 빈 것과 아직 채워넣기 전인 것을 확실하게 구분해야 함
        if cls.press is None:
            return cls.objects.filter(content='')[:299]

        return cls.objects.filter(content='')

    def get_admin_change_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])

    def browser_agent(self):
        return self.press.browser_agent()

    @property
    def link_url(self):
        return self.url


    
    
    def get_admin_change_url(self):
        return reverse('admin:%s_%s_change' %
                       (self._meta.app_label, super(self.__class__, self)._meta.model_name), args=[self.id])

    def article_soup(self, body):
        soup = BeautifulSoup(body, 'lxml')
        self.soup_article = soup.select_one(self.selector_article)

        return self.soup_article

    def fill_article_content(self):
        if self.content in [None, ARTICLE_SPECIAL]:
            return

        # if self.content == '' or self.content == ' ':
        #     return
        #

        try:
            for selector in self.decompose_element:
                _element = self.soup_article_content.select_one(selector)

                if _element is not None:
                    _element.decompose()

            # 기자 email 을 찾으려면 마지막 문단을 찾아야 함

            _content = []
            for string in self.soup_article_content.stripped_strings:
                _content.append(string)

            if len(_content) == 0:
                self.content = ARTICLE_CONTENT_NONE
            else:
                self.content = "\n".join(_content)

        except AttributeError as e:
            print(e)

        self.save()
        
    
    """