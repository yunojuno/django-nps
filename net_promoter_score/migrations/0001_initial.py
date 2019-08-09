# -*- coding: utf-8 -*-


from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="UserScore",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("timestamp", models.DateTimeField()),
                (
                    "score",
                    models.IntegerField(
                        default=-1,
                        help_text="0-6=Detractor; 7-8=Neutral; 9-10=Promoter",
                        db_index=True,
                    ),
                ),
                (
                    "reason",
                    models.TextField(help_text="Reason for the score", blank=True),
                ),
                (
                    "group",
                    models.CharField(
                        default="unknown",
                        help_text="Detractor, neutral or promoter.",
                        max_length=10,
                        db_index=True,
                        choices=[
                            ("unknown", "No answer"),
                            ("detractor", "Detractor (0-6)"),
                            ("neutral", "Neutral (7-8)"),
                            ("promoter", "Promoter (9-10)"),
                        ],
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                        related_name="nps_scores",
                    ),
                ),
            ],
        )
    ]
