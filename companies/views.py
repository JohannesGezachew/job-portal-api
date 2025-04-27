from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company
from .serializers import CompanySerializer, CompanyDetailSerializer


class IsEmployerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow employers to create/edit companies.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to employers
        return request.user and request.user.is_authenticated and request.user.user_type == 'employer'


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['industry', 'location']
    search_fields = ['name', 'description', 'industry']
    ordering_fields = ['name', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompanyDetailSerializer
        return CompanySerializer
    
    def perform_create(self, serializer):
        # Set the creator of the company
        company = serializer.save()
        self.request.user.company = company
        self.request.user.save()
