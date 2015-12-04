# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'net_promoter_score.views',
    url(r'^score/$', 'post_score', name="post_score"),
)
