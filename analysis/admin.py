from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from analysis.models import ListIgnoreRule, MatchRule


class ListIgnoreRuleAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'enable', 'positive', 'negative')
    list_display_links = ('id', 'title',)
    list_filter = ('enable',)
    search_fields = ('title', 'positive', 'negative')


class MatchRuleAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'enable', 'positive', 'negative', 'order', 'check_content')
    list_display_links = ('id', 'title',)
    list_filter = ('enable',)
    search_fields = ('title', 'positive', 'negative')


admin.site.register(ListIgnoreRule, ListIgnoreRuleAdmin)
admin.site.register(MatchRule, MatchRuleAdmin)
