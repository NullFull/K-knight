from django.contrib import admin

from organization.models import ThePress, Reporter, ReporterDetail, ArticleReporter

admin.site.register(ThePress)
admin.site.register(Reporter)
admin.site.register(ReporterDetail)
admin.site.register(ArticleReporter)
