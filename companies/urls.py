from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'companies'

router = DefaultRouter()
router.register(r'', views.CompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 