from django.contrib import admin

from .models import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('participant_id', 'name', 'rank', 'result')
    list_filter = ('rank',)
    search_fields = ('participant_id', 'name')
    ordering = ('rank', 'participant_id')
