import unittest

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.test import TestCase

from net_promoter_score.models import UserScore
from net_promoter_score.signals import new_nps_score


class SignalTests(TestCase):
    def test_new_nps_score_sent(self):
        handler = unittest.mock.Mock()
        new_nps_score.connect(handler)

        score = UserScore()
        post_save.send(sender=UserScore, instance=score, created=True)
        handler.assert_called_once_with(
            signal=new_nps_score, sender=UserScore, instance=score
        )

    def test_new_nps_score_not_sent__not_created(self):
        handler = unittest.mock.Mock()
        new_nps_score.connect(handler)

        score = UserScore()
        post_save.send(sender=UserScore, instance=score, created=False)
        assert handler.call_count == 0

    def test_new_nps_score_not_sent__other_model(self):
        handler = unittest.mock.Mock()
        new_nps_score.connect(handler)

        user = get_user_model()()
        post_save.send(sender=user.__class__, instance=user, created=False)
        assert handler.call_count == 0
