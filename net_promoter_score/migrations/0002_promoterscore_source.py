# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("net_promoter_score", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="userscore",
            name="source",
            field=models.CharField(
                help_text="Source of user score, used for filtering results, e.g. 'app', 'web', 'email'.",
                max_length=20,
                blank=True,
            ),
        )
    ]
