from django.contrib.auth import get_user_model
from django.test import TransactionTestCase

from ..forms import UserScoreForm


class UserScoreFormTests(TransactionTestCase):

    """Test suite for promoter score forms."""

    def setUp(self):
        self.user = get_user_model().objects.create_user("zoidberg")

    def validate_form(self, data):
        form = UserScoreForm(data=data, user=self.user)
        return form.is_valid()

    def test_clean_valid_score(self):
        for i in range(0, 11):
            self.assertTrue(self.validate_form(data={"score": i}))

    def test_clean_invalid_score(self):
        for i in (-2, 11, "", None):
            self.assertFalse(self.validate_form(data={"score": i}))

    def test_clean_unicode_reason(self):
        data = {"score": 0, "reason": "√" * 512}
        self.assertTrue(self.validate_form(data=data))

    def test_clean_invalid_reason(self):
        data = {"score": 0, "reason": "√" * 513}
        self.assertFalse(self.validate_form(data))

    def test_save(self):
        data = {"score": 0, "reason": "∂ƒ©˙∆˚¬"}
        form = UserScoreForm(data=data, user=self.user)
        score = form.save()
        self.assertIsNotNone(score)
        self.assertEqual(score.user, self.user)
        self.assertEqual(score.score, 0)
        self.assertEqual(score.reason, data["reason"])
