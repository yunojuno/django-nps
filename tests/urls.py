from django.contrib import admin

try:
    from django.urls import include, re_path
except ImportError:
    from django.conf.urls import include
    from django.conf.urls import url as re_path

admin.autodiscover()

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^nps/", include("net_promoter_score.urls")),
]
