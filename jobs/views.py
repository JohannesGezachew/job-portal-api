from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Job, JobApplication, Bookmark
from .serializers import (
    JobSerializer, JobDetailSerializer,
    JobApplicationSerializer, BookmarkSerializer
)


class IsEmployerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow employers to create/edit jobs.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to employers
        return request.user and request.user.is_authenticated and request.user.user_type == 'employer'

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only the job poster can edit or delete it
        return obj.posted_by == request.user


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter(is_active=True).order_by('-posted_at')
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['job_type', 'experience_level', 'location', 'company']
    search_fields = ['title', 'description', 'skills_required', 'company__name']
    ordering_fields = ['posted_at', 'salary_min', 'salary_max']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return JobDetailSerializer
        return JobSerializer
    
    def perform_create(self, serializer):
        # Set the job poster to the current user
        serializer.save(posted_by=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_jobs(self, request):
        """Return jobs posted by the current employer"""
        if request.user.user_type != 'employer':
            return Response(
                {"error": "Only employers can view their posted jobs"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        jobs = Job.objects.filter(posted_by=request.user).order_by('-posted_at')
        page = self.paginate_queryset(jobs)
        
        if page is not None:
            serializer = JobSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # If user is an employer, show applications for their job postings
        if user.user_type == 'employer':
            return JobApplication.objects.filter(job__posted_by=user).order_by('-applied_at')
        
        # If user is a job seeker, show their applications
        return JobApplication.objects.filter(applicant=user).order_by('-applied_at')
    
    def perform_create(self, serializer):
        job_id = self.request.data.get('job')
        job = get_object_or_404(Job, id=job_id)
        
        # Check if user has already applied
        if JobApplication.objects.filter(job=job, applicant=self.request.user).exists():
            return Response(
                {"error": "You have already applied for this job"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user is a job seeker
        if self.request.user.user_type != 'job_seeker':
            return Response(
                {"error": "Only job seekers can apply for jobs"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.save(applicant=self.request.user)


class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        job_id = self.request.data.get('job')
        job = get_object_or_404(Job, id=job_id)
        
        # Check if user has already bookmarked this job
        if Bookmark.objects.filter(job=job, user=self.request.user).exists():
            return Response(
                {"error": "You have already bookmarked this job"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'], url_path='toggle/(?P<job_id>[^/.]+)')
    def toggle_bookmark(self, request, job_id=None):
        """Toggle bookmark status for a job"""
        job = get_object_or_404(Job, id=job_id)
        bookmark = Bookmark.objects.filter(job=job, user=request.user).first()
        
        if bookmark:
            bookmark.delete()
            return Response({"status": "Bookmark removed"}, status=status.HTTP_200_OK)
        else:
            Bookmark.objects.create(job=job, user=request.user)
            return Response({"status": "Bookmark added"}, status=status.HTTP_201_CREATED)
