from django.contrib import admin
from .models import Job, JobApplication, Bookmark

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'posted_at', 'is_active')
    list_filter = ('job_type', 'experience_level', 'is_active', 'company')
    search_fields = ('title', 'description', 'company__name', 'location')
    date_hierarchy = 'posted_at'


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('job__title', 'applicant__username')
    date_hierarchy = 'applied_at'


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('job', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('job__title', 'user__username')
