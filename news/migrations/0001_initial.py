# Generated by Django 2.2.6 on 2019-10-28 18:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0002_auto_20191028_1701'),
        ('analysis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='절대 주소')),
                ('deleted', models.BooleanField(default=False, verbose_name='삭제된 기사')),
                ('human_result_title', models.BooleanField(default=False, verbose_name='제목 사람 판단 결과')),
                ('human_result_content', models.BooleanField(default=False, verbose_name='내용 사람 판단 결과')),
                ('perceived_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='시스템에서 인지한 시간')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='기사 작성 시간')),
                ('updated_at', models.DateTimeField(default=None, verbose_name='기사 업데이트 시간')),
                ('com_result_content', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='com_result_content_rule_id', to='analysis.MatchRule')),
                ('com_result_title', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='com_result_title_rule_id', to='analysis.MatchRule')),
                ('press', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.ThePress')),
            ],
        ),
    ]
