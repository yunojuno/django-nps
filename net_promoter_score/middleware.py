"""
NPS middleware used to set request attrs and cookies.

When determining whether to display the NPS survey to user, we cache
the output (True|False) so that we don't have to do a database lookup
on each request. This value is added to the user session (so a max
of one lookup per session.

"""
from __future__ import annotations

from typing import Callable

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest, HttpResponse

from .utils import show_nps


class NPSMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if not hasattr(request, "user"):
            raise ImproperlyConfigured(
                "Missing middleware: "
                "'django.contrib.auth.middleware.AuthenticationMiddleware'"
            )
        if request.user.is_authenticated:
            request.show_nps = show_nps(request)
        else:
            request.show_nps = False

        return self.get_response(request)
