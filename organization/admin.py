from django.contrib import admin

from organization.models import ThePress, Reporter, ReporterDetail

admin.site.register(ThePress)
admin.site.register(Reporter)
admin.site.register(ReporterDetail)
