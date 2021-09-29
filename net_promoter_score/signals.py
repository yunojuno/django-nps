from __future__ import annotations

from typing import Any

from django.db.models.signals import post_save
from django.dispatch import Signal, receiver

from .models import UserScore

# custom signal sent when a new score is submitted
# providing_args=["instance"]
new_nps_score = Signal()


@receiver(post_save, sender=UserScore)
def on_new_score(
    sender: type[UserScore], instance: UserScore, created: bool, **kwargs: Any
) -> None:
    # this is a pass-through that filters just new objects
    if not created:
        return
    new_nps_score.send(sender=sender, instance=instance)
