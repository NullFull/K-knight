# Generated by Django 2.2.6 on 2019-10-28 18:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20191028_1821'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='이름 판단 근거')),
                ('email', models.CharField(max_length=128, verbose_name='이메일 판단 근거')),
                ('title', models.CharField(max_length=128, verbose_name='제목')),
                ('content', models.TextField(default='', verbose_name='내용')),
                ('perceived_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='시스템에서 인지한 시간')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='기사 작성 시간')),
                ('updated_at', models.DateTimeField(default=None, verbose_name='기사 업데이트 시간')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Article')),
            ],
        ),
    ]
