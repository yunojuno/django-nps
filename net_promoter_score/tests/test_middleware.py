# -*- coding: utf-8 -*-
"""Tests for net_promoter_score.middleware."""
import mock

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TransactionTestCase, RequestFactory

from net_promoter_score.models import UserScore
from net_promoter_score.middleware import NPSMiddleware


class MiddlewareTests(TransactionTestCase):

    """Test suite for middleware."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user('zoidberg')
        self.score = UserScore(user=self.user, score=10).save()
        self.middleware = NPSMiddleware()

    def test_process_request(self):
        request = self.factory.get('/')
        request.user = self.user
        with mock.patch('net_promoter_score.settings.NPS_DISPLAY_FUNCTION', lambda r: True):
            resp = self.middleware.process_request(request)
            self.assertIsNone(resp)
            self.assertTrue(request.show_nps)

            # verify that unauthenticated users always return False
            request.user = AnonymousUser()
            resp = self.middleware.process_request(request)
            self.assertIsNone(resp)
            self.assertFalse(request.show_nps)
