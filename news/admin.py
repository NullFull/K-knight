from django.contrib import admin

from news.models import Article, ArticleContent

admin.site.register(Article)
admin.site.register(ArticleContent)
