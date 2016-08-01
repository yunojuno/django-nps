# -*- coding: utf-8 -*-

from net_promoter_score import settings


def show_nps(request):
    """Return True if the NPS survey should be shown to the request user.

    This is a dynamic function that uses the request object to determine
    whether to display the survey. It defaults to a basic function that
    looks up the last time the user was shown the survey, so that each
    user is only shown it every X days. This should be overridden in the
    Django settings to provide more sophisticated analysis - users with
    different profiles may be surveyed more/less frequently, and you may
    wish to survery based on previous answers.

    """
    return settings.NPS_DISPLAY_FUNCTION(request)
