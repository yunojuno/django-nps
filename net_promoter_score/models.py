from __future__ import annotations

from typing import Any

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.timezone import now as tz_now


def score_group(score: int) -> str:
    """Return 'detractor', 'neutral' or 'promoter'."""
    if not isinstance(score, int):
        raise ValueError("Score must be an integer value")
    if score < -1:
        raise ValueError("Score cannot be less than -1")
    if score > 10:
        raise ValueError("Score cannot be greater than 10")

    if score == -1:
        return UserScore.GROUP_UNKNOWN
    elif score < 7:
        return UserScore.GROUP_DETRACTOR
    elif score < 9:
        return UserScore.GROUP_NEUTRAL
    else:
        return UserScore.GROUP_PROMOTER


class UserScoreQuerySet(models.query.QuerySet):
    """Custom UserScore queryset - calculates the NPS."""

    def promoters(self) -> UserScoreQuerySet:
        """Filter queryset by promoters."""
        return self.filter(group=UserScore.GROUP_PROMOTER)

    def detractors(self) -> UserScoreQuerySet:
        """Filter queryset by detractors."""
        return self.filter(group=UserScore.GROUP_DETRACTOR)

    def neutrals(self) -> UserScoreQuerySet:
        """Filter queryset by neutrals."""
        return self.filter(group=UserScore.GROUP_NEUTRAL)

    def net_promoter_score(self) -> float:
        """
        Calculate the NPS score from a set of UserScore objects.

        The NPS is the % of promoters - % of detractors (ignoring
        neutrals).

        """
        promoters = self.promoters().count()
        detractors = self.detractors().count()
        neutrals = self.neutrals().count()
        total = promoters + detractors + neutrals
        return (100.0 * (promoters - detractors)) / total

    def most_recent_user_score(self, user: AbstractBaseUser) -> UserScore:
        """Return the most recent user UserScore."""
        return self.filter(user=user).order_by("-id").first()

    def days_since_user_score(self, user: AbstractBaseUser) -> int:
        """
        Return the number of days since the User last submitted a score.

        Returns -1 if the user has never been asked.

        """
        score = self.most_recent_user_score(user)
        return score.elapsed if score else -1


class UserScore(models.Model):
    """Records the NPS score given by a user."""

    GROUP_UNKNOWN = "unknown"
    GROUP_PROMOTER = "promoter"
    GROUP_DETRACTOR = "detractor"
    GROUP_NEUTRAL = "neutral"

    GROUP_CHOICES = (
        (GROUP_UNKNOWN, "No answer"),
        (GROUP_DETRACTOR, "Detractor (0-6)"),
        (GROUP_NEUTRAL, "Neutral (7-8)"),
        (GROUP_PROMOTER, "Promoter (9-10)"),
    )

    class Meta:
        app_label = "net_promoter_score"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="nps_scores",
    )
    timestamp = models.DateTimeField()
    score = models.IntegerField(
        default=-1,
        blank=False,
        null=False,
        # validators=[MinValueValidator(-1), MaxValueValidator(10)],
        help_text="0-6=Detractor; 7-8=Neutral; 9-10=Promoter",
        db_index=True,
    )
    reason = models.TextField(blank=True, help_text="Reason for the score")
    # this field is calculated from the score, but is denormalised into
    # a separate property to make it easier to report on. It's kept in
    # sync in the save method.
    group = models.CharField(
        max_length=10,
        default=GROUP_UNKNOWN,
        choices=GROUP_CHOICES,
        help_text="Detractor, neutral or promoter.",
        db_index=True,
    )
    source = models.CharField(
        max_length=20,
        blank=True,
        help_text=(
            "Source of user score, used for filtering results, "
            "e.g. 'app', 'web', 'email'."
        ),
    )

    objects = UserScoreQuerySet.as_manager()

    def __str__(self) -> str:
        if self.timestamp:
            return f"{self.group} ({self.score}/10), {self.timestamp.date()}"
        else:
            return f"{self.group} ({self.score}/10), unsaved"

    def __repr__(self) -> str:
        return f"<UserScore: id={self.pk} score={self.score}>"

    def save(self, *args: Any, **kwargs: Any) -> UserScore:
        """Set the timestamp and group attrs."""
        self.timestamp = self.timestamp or tz_now()
        self.group = score_group(self.score)
        super().save(*args, **kwargs)
        return self

    def json(self) -> dict:
        """Return JSON-serializable form of the object."""
        if not self.id:
            raise ValueError("Score must be saved before calling json().")
        return {
            "id": self.id,
            "user": self.user.pk,
            "score": self.score,
            "group": self.group,
        }

    @property
    def is_promoter(self) -> bool:
        return self.group == UserScore.GROUP_PROMOTER

    @property
    def is_detractor(self) -> bool:
        return self.group == UserScore.GROUP_DETRACTOR

    @property
    def is_neutral(self) -> bool:
        return self.group == UserScore.GROUP_NEUTRAL

    @property
    def is_unknown(self) -> bool:
        return self.group == UserScore.GROUP_UNKNOWN

    @property
    def elapsed(self) -> int:
        """Return number of days since the score was submitted."""
        return (tz_now().date() - self.timestamp.date()).days
