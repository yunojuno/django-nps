# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('score', models.IntegerField(default=-1, help_text=b'0-6=Detractor; 7-8=Neutral; 9-10=Promoter', db_index=True)),
                ('reason', models.TextField(help_text=b'Reason for the score', blank=True)),
                ('group', models.CharField(default=b'unknown', help_text='Detractor, neutral or promoter.', max_length=10, db_index=True, choices=[(b'unknown', b'No answer'), (b'detractor', b'Detractor (0-6)'), (b'neutral', b'Neutral (7-8)'), (b'promoter', b'Promoter (9-10)')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
