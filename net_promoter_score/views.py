# -*- coding:utf-8 -*-
"""net_promoter_score views."""
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from net_promoter_score.forms import UserScoreForm


@require_POST
@user_passes_test(lambda u: u.is_authenticated())
def post_score(request):
    """POST handler for NPS scores.

    Returns a JSON object, which includes a 'success' key that is True/False.
    If success is True, the response will also contain a 'score' value that
    is the UserScore.json() object.

        {
          "success": True,
          "score": {"id": 1, "user": 1, "score": 0, "group": "detractor"}
        }

    If success is False, the response will contains an 'errors' list:

        {
          "success": False,
          "errors": [["score", "Score must be between 0-10"]]
        }

    """
    form = UserScoreForm(request.POST, user=request.user)
    if form.is_valid():
        score = form.save()
        return JsonResponse({'success': True, 'score': score.json()}, status=201)  # noqa
    else:
        errors = [(k, v[0]) for k, v in form.errors.items()]
        return JsonResponse({'success': False, 'errors': errors}, status=422)
