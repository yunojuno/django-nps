try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path

from . import views

app_name = "net_promoter_score"

urlpatterns = [re_path(r"^score/$", views.post_score, name="post_score")]
