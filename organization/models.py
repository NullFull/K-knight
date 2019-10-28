from django.db import models


class ThePress(models.Model):
    title = models.CharField('언론사 이름', max_length=128)
    main_url = models.URLField('대표 홈페이지', unique=True)
    mobile_url = models.URLField('모바일 홈페이지', unique=True)

    def __str__(self):
        return self.title


class Reporter(models.Model):
    pass


class ReporterDetail(models.Model):
    reporter = models.ForeignKey('Reporter', on_delete=models.CASCADE)
    press = models.ForeignKey('ThePress', on_delete=models.CASCADE)
    name = models.CharField('이름', max_length=32, default='', blank=True)
    email = models.EmailField('이메일', default='', blank=True)
    # 기자 공개 이미지 URL
