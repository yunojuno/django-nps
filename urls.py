# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin  # , staticfiles

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^nps/', include('net_promoter_score.urls',
        namespace="net_promoter_score")),
    # url(r'^static/(?P<path>.*)$', staticfiles.views.serve),
]
