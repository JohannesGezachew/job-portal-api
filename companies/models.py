from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField()
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    founded_year = models.IntegerField(blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        
    def __str__(self):
        return self.name
