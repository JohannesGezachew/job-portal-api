from rest_framework import serializers
from .models import Job, JobApplication, Bookmark
from companies.serializers import CompanySerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = '__all__'
        
    def get_company_name(self, obj):
        return obj.company.name


class JobDetailSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    application_count = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    has_applied = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = '__all__'
    
    def get_application_count(self, obj):
        return obj.applications.count()
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.bookmarks.filter(user=request.user).exists()
        return False
    
    def get_has_applied(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.applications.filter(applicant=request.user).exists()
        return False


class JobApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.SerializerMethodField()
    applicant_name = serializers.SerializerMethodField()
    
    class Meta:
        model = JobApplication
        fields = '__all__'
        
    def get_job_title(self, obj):
        return obj.job.title
    
    def get_applicant_name(self, obj):
        return f"{obj.applicant.first_name} {obj.applicant.last_name}"


class BookmarkSerializer(serializers.ModelSerializer):
    job_title = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Bookmark
        fields = '__all__'
        
    def get_job_title(self, obj):
        return obj.job.title
    
    def get_company_name(self, obj):
        return obj.job.company.name 