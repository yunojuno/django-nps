import datetime
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TransactionTestCase

from ..models import UserScore
from ..settings import NPS_DISPLAY_INTERVAL, default_display_function
from ..utils import show_nps


class FunctionTests(TransactionTestCase):

    """Test suite for misc functions."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user("zoidberg")
        self.score = UserScore(user=self.user, score=10).save()

    def test_display_to_user(self):
        request = self.factory.get("/")
        request.user = self.user
        with mock.patch(
            "net_promoter_score.settings.NPS_DISPLAY_FUNCTION", lambda r: True
        ):
            self.assertTrue(show_nps(request))
        with mock.patch(
            "net_promoter_score.settings.NPS_DISPLAY_FUNCTION", lambda r: False
        ):
            self.assertFalse(show_nps(request))

    def test_default_display_function(self):
        # test that the default function behaves as expected
        request = self.factory.get("/")
        request.user = self.user
        interval_func = UserScore.objects.days_since_user_score
        self.assertEqual(interval_func(self.user), 0)
        self.assertEqual(NPS_DISPLAY_INTERVAL, 30)

        # 0 days since survey - don't show
        self.assertFalse(default_display_function(request))

        # 30 days since survey - don't show
        self.score.timestamp = self.score.timestamp - datetime.timedelta(days=30)
        self.score.save()
        self.assertFalse(interval_func(self.user) > NPS_DISPLAY_INTERVAL)
        self.assertFalse(default_display_function(request))

        # 31 days since survey - *do* show
        self.score.timestamp = self.score.timestamp - datetime.timedelta(days=31)
        self.score.save()
        self.assertTrue(interval_func(self.user) > NPS_DISPLAY_INTERVAL)
        self.assertTrue(default_display_function(request))

        # never been surveyed - *do* show
        self.score.delete()
        self.assertEqual(interval_func(self.user), -1)
        self.assertTrue(default_display_function(request))
