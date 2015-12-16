# -*- coding: utf-8 -*-
"""NPS middleware used to set request attrs and cookies.

When determining whether to display the NPS survey to user, we cache
the output (True|False) so that we don't have to do a database lookup
on each request. This value is added to the user session (so a max
of one lookup per session.

"""
from net_promoter_score import show_nps


class NPSMiddleware(object):
    """Add show_nps attr to the user session."""

    def process_request(self, request):
        request.show_nps = show_nps(request)
        return None
