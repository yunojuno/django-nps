# -*- coding: utf-8 -*-
"""Django app for managing Net Promoter Score data.

The NPS is a measure of customer loyalty that is measured by asking your
customers a singe question:

    How likely is it that you would recommend our company/product/service
    to a friend or colleague?"

The answer to this question is a number from 0-10 (inclusive). These scores
are then broken out into three distinct groups: 'detractors' (0-6), 'neutral'
(7-8) and 'promoters' (9-10). The NPS is then the difference between the
number of promoters and detractors (as a percentage of the whole population).

For example, if you ask 100 people, and you get the following results:

    detractors: 20
    neutrals:   10
    promoters:  70

Then your NPS is 70 - 20 = 50.

This app is used to store the individual scores, and calculate the NPS based
on these. It does not contain any templates for displaying the question form,
neither does it put any restriction around how often you ask the question, or
to whom. It is up to the app developer to determine how this should work -
each score is timestamped and linked to a Django User object, so you can
easily work out the time elapsed since the last time they were asked.

"""
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
