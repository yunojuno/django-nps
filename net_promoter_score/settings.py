"""
Default settings for net_promoter_score.

Override these settings in the Django settings if required.

"""

from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest

from .models import UserScore


def default_display_function(request: HttpRequest) -> bool:
    """
    Return default NPS display function.

    The default display function uses the days_since_user_score to determine
    whether to show NPS to the user. If the interval since the last survey is
    more than the NPS_DISPLAY_INTERVAL, *or* they've never been surveyed, then
    return True.

    """
    if not hasattr(request, "user"):
        raise ImproperlyConfigured(
            "Missing middleware: "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'"
        )
    interval = UserScore.objects.days_since_user_score(request.user)
    if interval == -1:
        return True
    if interval > NPS_DISPLAY_INTERVAL:
        return True
    return False


# default display interval is 30 days
NPS_DISPLAY_INTERVAL = getattr(settings, "NPS_DISPLAY_INTERVAL", 30)
# default display function is to show every 30 days, ignoring any user attrs.
NPS_DISPLAY_FUNCTION = getattr(
    settings, "NPS_DISPLAY_FUNCTION", default_display_function
)
