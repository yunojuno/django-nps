# -*- coding: utf-8 -*-
from django.contrib import admin

from net_promoter_score.models import PromoterScore


class PromoterScoreAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'timestamp',
        'score',
        'group'
    )
    list_filter = (
        'timestamp',
        'group'
    )
    readonly_fields = (
        'user',
        'timestamp',
        'score',
        'group',
        'reason'
    )

admin.site.register(PromoterScore, PromoterScoreAdmin)
