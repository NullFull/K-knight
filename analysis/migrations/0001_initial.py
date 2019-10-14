# Generated by Django 2.2.6 on 2019-10-14 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ListIgnoreRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='룰 제목')),
                ('enable', models.BooleanField(default=True, verbose_name='동작')),
                ('positive', models.CharField(max_length=200, verbose_name='매칭 룰')),
                ('negative', models.CharField(blank=True, max_length=200, verbose_name='제외 룰')),
                ('desc', models.TextField(blank=True, verbose_name='사유')),
                ('memo', models.TextField(blank=True, verbose_name='관리 기록')),
            ],
        ),
        migrations.CreateModel(
            name='MatchRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='룰 제목')),
                ('enable', models.BooleanField(default=True, verbose_name='동작')),
                ('positive', models.CharField(max_length=200, verbose_name='매칭 룰')),
                ('negative', models.CharField(blank=True, max_length=200, verbose_name='제외 룰')),
                ('desc', models.TextField(blank=True, verbose_name='사유')),
                ('memo', models.TextField(blank=True, verbose_name='관리 기록')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='적용 순서')),
                ('check_content', models.BooleanField(default=True, verbose_name='본문 체크')),
            ],
        ),
    ]
