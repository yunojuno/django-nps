# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth import get_user_model
from django.test import TransactionTestCase

from net_promoter_score.models import UserScore, score_group


class UserScoreModelTests(TransactionTestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('zoidberg')
        self.user2 = get_user_model().objects.create_user('nixon')

    def test_defaults(self):
        score = UserScore(user=self.user)
        self.assertEqual(score.user, self.user)
        self.assertEqual(score.timestamp, None)
        self.assertEqual(score.score, -1)
        self.assertEqual(score.reason, "")
        self.assertEqual(score.source, "")
        self.assertEqual(score.group, UserScore.GROUP_UNKNOWN)
        score.save()
        self.assertIsNotNone(score.timestamp)
        # confirm that the group is recalculated correctly
        score.score = 1
        score.save()
        self.assertEqual(score.group, UserScore.GROUP_DETRACTOR)

    def test_strings(self):
        unicode_username = u"åß∂ƒ©˙∆˚"
        self.user.username = unicode_username
        self.user.save()
        score = UserScore(user=self.user, score=10)
        self.assertIsNotNone(unicode(score))
        self.assertIsNotNone(str(score))
        self.assertIsNotNone(repr(score))
        score.save()
        self.assertIsNotNone(unicode(score))
        self.assertIsNotNone(str(score))
        self.assertIsNotNone(repr(score))

    def test_functions(self):
        self.assertRaises(AssertionError, score_group, None)
        self.assertRaises(AssertionError, score_group, "None")
        self.assertRaises(AssertionError, score_group, -2)
        self.assertRaises(AssertionError, score_group, 11)
        vals = (
            (-1, UserScore.GROUP_UNKNOWN),
            (0, UserScore.GROUP_DETRACTOR),
            (1, UserScore.GROUP_DETRACTOR),
            (2, UserScore.GROUP_DETRACTOR),
            (3, UserScore.GROUP_DETRACTOR),
            (4, UserScore.GROUP_DETRACTOR),
            (5, UserScore.GROUP_DETRACTOR),
            (6, UserScore.GROUP_DETRACTOR),
            (7, UserScore.GROUP_NEUTRAL),
            (8, UserScore.GROUP_NEUTRAL),
            (9, UserScore.GROUP_PROMOTER),
            (10, UserScore.GROUP_PROMOTER),
        )
        for val, group in vals:
            self.assertEqual(score_group(val), group)


class UserScoreQuerySetTests(TransactionTestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('zoidberg')
        self.psX = UserScore(user=self.user, score=-1).save()
        self.ps0 = UserScore(user=self.user, score=0).save()
        self.ps1 = UserScore(user=self.user, score=1).save()
        self.ps2 = UserScore(user=self.user, score=2).save()
        self.ps3 = UserScore(user=self.user, score=3).save()
        self.ps4 = UserScore(user=self.user, score=4).save()
        self.ps5 = UserScore(user=self.user, score=5).save()
        self.ps6 = UserScore(user=self.user, score=6).save()
        self.ps7 = UserScore(user=self.user, score=7).save()
        self.ps8 = UserScore(user=self.user, score=8).save()
        self.ps9 = UserScore(user=self.user, score=9).save()
        self.ps10 = UserScore(user=self.user, score=10).save()

    def test_detractors(self):
        detractors = UserScore.objects.detractors()
        self.assertEqual(detractors.count(), 7)
        self.assertTrue(self.ps0 in detractors)
        self.assertTrue(self.ps1 in detractors)
        self.assertTrue(self.ps2 in detractors)
        self.assertTrue(self.ps3 in detractors)
        self.assertTrue(self.ps4 in detractors)
        self.assertTrue(self.ps5 in detractors)
        self.assertTrue(self.ps6 in detractors)

    def test_neutrals(self):
        neutrals = UserScore.objects.neutrals()
        self.assertEqual(neutrals.count(), 2)
        self.assertTrue(self.ps7 in neutrals)
        self.assertTrue(self.ps8 in neutrals)

    def test_promoters(self):
        promoters = UserScore.objects.promoters()
        self.assertEqual(promoters.count(), 2)
        self.assertTrue(self.ps9 in promoters)
        self.assertTrue(self.ps10 in promoters)

    def test_net_promoter_score(self):
        scores = UserScore.objects.all()
        expected = (2.0 - 7.0) / 11 * 100
        self.assertEqual(scores.net_promoter_score(), expected)

    def test_most_recent_user_score(self):
        score = UserScore.objects.most_recent_user_score(self.user)
        self.assertEqual(score, self.ps10)

    def test_days_since_user_score(self):
        score = UserScore.objects.most_recent_user_score(self.user)
        # need to delete all the others
        UserScore.objects.exclude(id=score.id).delete()
        self.assertEqual(UserScore.objects.days_since_user_score(self.user), 0)

        # set the date back 7 days
        today = datetime.date.today()
        score.timestamp = today - datetime.timedelta(days=7)
        score.save()
        self.assertEqual(UserScore.objects.days_since_user_score(self.user), 7)

        # delete all scores for the user
        score.delete()
        self.assertEqual(UserScore.objects.days_since_user_score(self.user), -1)
