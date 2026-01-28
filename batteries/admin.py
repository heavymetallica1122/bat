from django.contrib import admin
from .models import BatterySubmission, RecyclableType


@admin.register(RecyclableType)
class RecyclableTypeAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'unit', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)


@admin.register(BatterySubmission)
class BatterySubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'recyclable_type', 'quantity', 'city', 'date_submitted')
    list_filter = ('date_submitted', 'user', 'city', 'recyclable_type')
    search_fields = ('user__username',)
    date_hierarchy = 'date_submitted'
