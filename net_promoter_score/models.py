# -*- coding: utf-8 -*-
"""net_promoter_score models."""
from django.db import models
from django.conf import settings
from django.utils.timezone import now as tz_now


def score_group(score):
    """Return 'detractor', 'neutral' or 'promoter'."""
    assert isinstance(score, int), "Score must be an integer value"
    assert score >= -1, "Score cannot be less than -1"
    assert score <= 10, "Score cannot be greater than 10"
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

    def promoters(self):
        """Filter queryset by promoters."""
        return self.filter(group=UserScore.GROUP_PROMOTER)

    def detractors(self):
        """Filter queryset by detractors."""
        return self.filter(group=UserScore.GROUP_DETRACTOR)

    def neutrals(self):
        """Filter queryset by neutrals."""
        return self.filter(group=UserScore.GROUP_NEUTRAL)

    def net_promoter_score(self):
        """Calculate the NPS score from a set of UserScore objects.

        The NPS is the % of promoters - % of detractors (ignoring
        neutrals).

        """
        promoters = self.promoters().count()
        detractors = self.detractors().count()
        neutrals = self.neutrals().count()
        total = promoters + detractors + neutrals
        return (100.0 * (promoters - detractors)) / total

    def most_recent_user_score(self, user):
        """Return the most recent user UserScore."""
        return self.filter(user=user).order_by('-id').first()

    def days_since_user_score(self, user):
        """Return the number of days since the User last submitted a score.

        Returns -1 if the user has never been asked.

        """
        score = self.most_recent_user_score(user)
        if score is None:
            return -1
        else:
            return (tz_now().date() - score.timestamp.date()).days


class UserScore(models.Model):

    """Records the NPS score given by a user."""

    GROUP_UNKNOWN = 'unknown'
    GROUP_PROMOTER = 'promoter'
    GROUP_DETRACTOR = 'detractor'
    GROUP_NEUTRAL = 'neutral'

    GROUP_CHOICES = (
        (GROUP_UNKNOWN, 'No answer'),
        (GROUP_DETRACTOR, 'Detractor (0-6)'),
        (GROUP_NEUTRAL, 'Neutral (7-8)'),
        (GROUP_PROMOTER, 'Promoter (9-10)')
    )

    class Meta:
        app_label = 'net_promoter_score'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True)
    timestamp = models.DateTimeField()
    score = models.IntegerField(
        default=-1,
        blank=False, null=False,
        # validators=[MinValueValidator(-1), MaxValueValidator(10)],
        help_text="0-6=Detractor; 7-8=Neutral; 9-10=Promoter",
        db_index=True,
    )
    reason = models.TextField(
        blank=True,
        help_text="Reason for the score"
    )
    # this field is calculated from the score, but is denormalised into
    # a separate property to make it easier to report on. It's kept in
    # sync in the save method.
    group = models.CharField(
        max_length=10,
        default=GROUP_UNKNOWN,
        choices=GROUP_CHOICES,
        help_text=u"Detractor, neutral or promoter.",
        db_index=True
    )
    source = models.CharField(
        max_length=20,
        blank=True,
        help_text=(
            "Source of user score, used for filtering results, "
            "e.g. 'app', 'web', 'email'."
        )
    )

    objects = UserScoreQuerySet.as_manager()

    def __unicode__(self):
        if self.timestamp:
            return u"%s is a %s (%s/10), %s" % (
                self.user, self.group, self.score, self.timestamp.date()
            )
        else:
            return u"%s is a %s (%s/10), unsaved" % (
                self.user, self.group, self.score
            )

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return "<UserScore: id=%s user=%s score=%s>" % (
            self.id, self.user.id, self.score
        )

    def save(self, *args, **kwargs):
        """Set the timestamp and group attrs."""
        self.timestamp = self.timestamp or tz_now()
        self.group = score_group(self.score)
        super(UserScore, self).save(*args, **kwargs)
        return self

    def json(self):
        """Response JSON-serializable form of the object."""
        assert self.id is not None, "Score must be saved before calling json()."
        return {
            'id': self.id,
            'user': self.user.id,
            'score': self.score,
            'group': self.group
        }
