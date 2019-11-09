import re

from django.conf import settings
from django.db import models


def _match(rule, string):
    if rule == '' or rule is None:
        return None

    # TODO: 정규식이 아닌 경우도 잘 동작할 수 있게 다시 수정

    if string is None:
        return None

    p = re.compile(rule)
    lines = string.splitlines()
    for line in lines:
        if p.search(line):
            return line

    return None


class ListIgnoreRule(models.Model):
    title = models.CharField(max_length=200, verbose_name='룰 제목')
    enable = models.BooleanField(default=True, verbose_name='동작')
    positive = models.CharField(max_length=200, verbose_name='매칭 룰')
    negative = models.CharField(max_length=200, blank=True, verbose_name='제외 룰')
    desc = models.TextField(blank=True, verbose_name='사유')
    memo = models.TextField(blank=True, verbose_name='관리 기록')

    def __str__(self):
        return self.title

    def match(self, string):
        if not _match(self.positive, string):
            return False

        if _match(self.negative, string):
            return False

        return True

    @classmethod
    def match_all(cls, string):
        for rule in cls.objects.filter(enable=True):
            if rule.match(string):
                return rule

        return None


class MatchRule(models.Model):
    title = models.CharField(max_length=200, verbose_name='룰 제목')
    enable = models.BooleanField(default=True, verbose_name='동작')
    positive = models.CharField(max_length=200, verbose_name='매칭 룰')
    negative = models.CharField(max_length=200, blank=True, verbose_name='제외 룰')
    desc = models.TextField(blank=True, verbose_name='사유')
    memo = models.TextField(blank=True, verbose_name='관리 기록')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='적용 순서')
    check_content = models.BooleanField(default=True, verbose_name='본문 체크')

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        if self.order:
            super(self.__class__, self).save()
            return

        # TODO: 마지막에서 하나 위로 넣어줘야 할 듯
        self.order = 0
        for rule in self.__class__.objects.all():
            if self.order < rule.order:
                self.order = rule.order

        self.order += 1
        super(self.__class__, self).save()

    def matched_line(self, string):
        line = _match(self.positive, string)
        if not line:
            return None

        if _match(self.negative, string):
            return None

        return line

    def match(self, article):
        matched_line = None

        line = self.matched_line(article.content)
        if line:
            matched_line = line
            article.result_system_content = self

        line = self.matched_line(article.title)
        if line:
            matched_line = line
            article.result_system_title = self

        if matched_line is None:
            return None

        article.save()

        if article.result_system_title:
            return matched_line

        if self.check_content:
            return matched_line

        return None

    @classmethod
    def match_all(cls, article):
        matched_rule = None

        for rule in cls.objects.filter(enable=True).order_by('-order', '-id'):
            if rule.match(article):
                matched_rule = rule

        if matched_rule is None:
            return None

        return matched_rule

#
# class AnalysisResult(models.Model):
#     # article = models.ForeignKey('ArticleContent', on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     com_result_title = models.ForeignKey('MatchRule', default=None, blank=True, verbose_name='제목 기준',
#                                          on_delete=models.SET_DEFAULT)
#     com_result_content = models.ForeignKey('MatchRule', default=None, blank=True, verbose_name='본문 기준',
#                                            on_delete=models.SET_DEFAULT)
#     human_result_title = models.BooleanField('제목 사람 판단 결과', default=False)
#     human_result_content = models.BooleanField('내용 사람 판단 결과', default=False)
#     created_at = models.DateTimeField('판단 시간', auto_now_add=True)
#     updated_at = models.DateTimeField('사람 판단 시간', default=None, blank=True)
