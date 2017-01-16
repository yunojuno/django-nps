# -*- coding: utf-8 -*-
"""NPS middleware used to set request attrs and cookies.

When determining whether to display the NPS survey to user, we cache
the output (True|False) so that we don't have to do a database lookup
on each request. This value is added to the user session (so a max
of one lookup per session.

"""
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    # Fallback for Django < 1.10
    MiddlewareMixin = object


from net_promoter_score.utils import show_nps


class NPSMiddleware(MiddlewareMixin):

    """Add show_nps attr to the user session."""

    def process_request(self, request):
        # force instantiation of the request.user SimpleLazyObject
        assert hasattr(request, 'user'), (
            "Missing middleware: "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'"
        )
        if request.user.is_authenticated():
            request.show_nps = show_nps(request)
        else:
            request.show_nps = False
        return None
