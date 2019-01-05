from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Candidate)
class CandiAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'name',
        'area'
    )
    

@admin.register(models.Poll)
class PollAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'area',
        'start_date',
        'end_date'
    )
    

@admin.register(models.Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display=(
        'can_for',
        'poll_for',
        'vote_count',
    )
    
@admin.register(models.Noti)
class NotiAdmin(admin.ModelAdmin):
    list_display=(
        'message',
    )