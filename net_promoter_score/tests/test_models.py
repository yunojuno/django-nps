# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase

from net_promoter_score.models import PromoterScore, score_group


class TestPromoterScoreModel(TransactionTestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='jared', password='foobar123'
        )
        self.user2 = self.user_model.objects.create_user(
            username='cole', email='cole@hotmail.com', password='foobar321'
        )

        self.user.save()
        self.user2.save()

    def test_defaults(self):
        score = PromoterScore(user=self.user)
        self.assertEqual(score.user, self.user)
        self.assertEqual(score.timestamp, None)
        self.assertEqual(score.score, -1)
        self.assertEqual(score.reason, "")
        self.assertEqual(score.group, PromoterScore.GROUP_UNKNOWN)
        score.save()
        self.assertIsNotNone(score.timestamp)
        # confirm that the group is recalculated correctly
        score.score = 1
        score.save()
        self.assertEqual(score.group, PromoterScore.GROUP_DETRACTOR)

    def test_strings(self):
        unicode_username = u"åß∂ƒ©˙∆˚"
        self.user.username = unicode_username
        self.user.save()
        score = PromoterScore(user=self.user, score=10)
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
            (-1, PromoterScore.GROUP_UNKNOWN),
            (0, PromoterScore.GROUP_DETRACTOR),
            (1, PromoterScore.GROUP_DETRACTOR),
            (2, PromoterScore.GROUP_DETRACTOR),
            (3, PromoterScore.GROUP_DETRACTOR),
            (4, PromoterScore.GROUP_DETRACTOR),
            (5, PromoterScore.GROUP_DETRACTOR),
            (6, PromoterScore.GROUP_DETRACTOR),
            (7, PromoterScore.GROUP_NEUTRAL),
            (8, PromoterScore.GROUP_NEUTRAL),
            (9, PromoterScore.GROUP_PROMOTER),
            (10, PromoterScore.GROUP_PROMOTER),
        )
        for val, group in vals:
            self.assertEqual(score_group(val), group)


class TestPromoterScoreQuerySet(TransactionTestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='jared', password='foobar123'
        )
        self.user.save()
        self.psX = PromoterScore(user=self.user, score=-1).save()
        self.ps0 = PromoterScore(user=self.user, score=0).save()
        self.ps1 = PromoterScore(user=self.user, score=1).save()
        self.ps2 = PromoterScore(user=self.user, score=2).save()
        self.ps3 = PromoterScore(user=self.user, score=3).save()
        self.ps4 = PromoterScore(user=self.user, score=4).save()
        self.ps5 = PromoterScore(user=self.user, score=5).save()
        self.ps6 = PromoterScore(user=self.user, score=6).save()
        self.ps7 = PromoterScore(user=self.user, score=7).save()
        self.ps8 = PromoterScore(user=self.user, score=8).save()
        self.ps9 = PromoterScore(user=self.user, score=9).save()
        self.ps10 = PromoterScore(user=self.user, score=10).save()

    def test_detractors(self):
        detractors = PromoterScore.objects.detractors()
        self.assertEqual(detractors.count(), 7)
        self.assertTrue(self.ps0 in detractors)
        self.assertTrue(self.ps1 in detractors)
        self.assertTrue(self.ps2 in detractors)
        self.assertTrue(self.ps3 in detractors)
        self.assertTrue(self.ps4 in detractors)
        self.assertTrue(self.ps5 in detractors)
        self.assertTrue(self.ps6 in detractors)

    def test_neutrals(self):
        neutrals = PromoterScore.objects.neutrals()
        self.assertEqual(neutrals.count(), 2)
        self.assertTrue(self.ps7 in neutrals)
        self.assertTrue(self.ps8 in neutrals)

    def test_promoters(self):
        promoters = PromoterScore.objects.promoters()
        self.assertEqual(promoters.count(), 2)
        self.assertTrue(self.ps9 in promoters)
        self.assertTrue(self.ps10 in promoters)

    def test_net_promoter_score(self):
        scores = PromoterScore.objects.all()
        expected = (2.0 - 7.0) / 11 * 100
        self.assertEqual(scores.net_promoter_score(), expected)

    def test_most_recent_user_score(self):
        score = PromoterScore.objects.most_recent_user_score(self.user)
        self.assertEqual(score, self.ps10)