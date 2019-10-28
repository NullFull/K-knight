from django.core.exceptions import ValidationError
from django.db import models


class ThePress(models.Model):
    title = models.CharField('언론사 이름', max_length=128)
    main_url = models.URLField('대표 홈페이지', unique=True)
    mobile_url = models.URLField('모바일 홈페이지', unique=True)

    def __str__(self):
        return self.title


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
