from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'jobs'

router = DefaultRouter()
router.register(r'jobs', views.JobViewSet)
router.register(r'applications', views.JobApplicationViewSet, basename='application')
router.register(r'bookmarks', views.BookmarkViewSet, basename='bookmark')

urlpatterns = [
    path('', include(router.urls)),
] 