# -*- coding: utf-8 -*-
import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import Client, TransactionTestCase, RequestFactory

from net_promoter_score.models import score_group, UserScore
from net_promoter_score.views import post_score


class UserScoreViewTests(TransactionTestCase):

    """Test suite for promoter score views."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'zoidberg', password="foo"
        )
        self.factory = RequestFactory()

    def test_valid_post_201(self):
        """Test that posting valid data returns the score and status_code 201."""
        data = {'score': 0, 'reason': u"√" * 512}
        request = self.factory.post('/', data)
        request.user = self.user
        resp = post_score(request)
        self.assertEqual(resp.status_code, 201)
        respj = json.loads(resp.content)
        self.assertEqual(respj['success'], True)
        self.assertEqual(respj['score']['user'], self.user.id)
        self.assertEqual(respj['score']['score'], data['score'])
        self.assertEqual(respj['score']['group'], score_group(data['score']))

    def test_invalid_post_422(self):
        """Test that posting invalid data returns the errors and status_code 422."""
        request = self.factory.post('/', {'score': -2})
        request.user = self.user
        resp = post_score(request)
        self.assertEqual(resp.status_code, 422)
        respj = json.loads(resp.content)
        self.assertEqual(respj['success'], False)
        self.assertEqual(respj['errors'], [[u'score', u'Score must be between 0-10']])  # noqa

    def test_client_post_anon_302(self):
        """Test posting as an AnonymousUser to the url."""
        client = Client()
        url = reverse('net_promoter_score:post_score')
        resp = client.post(url, data={'score': 0, 'reason': u"√" * 512})
        self.assertEqual(resp.status_code, 302)

    def test_client_post_auth_201(self):
        """Test posting as a User to the url."""
        client = Client()
        client.login(username='zoidberg', password='foo')
        url = reverse('net_promoter_score:post_score')
        resp = client.post(url, data={'score': 0, 'reason': u"√" * 512})
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(UserScore.objects.count(), 1)
