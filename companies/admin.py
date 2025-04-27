from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'location', 'created_at')
    list_filter = ('industry', 'location')
    search_fields = ('name', 'description', 'industry')
