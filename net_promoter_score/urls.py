# -*- coding: utf-8 -*-
from django.conf.urls import url

from net_promoter_score import views

urlpatterns = [
    url(
        r'^score/$',
        views.post_score,
        name="post_score"
    ),
]
