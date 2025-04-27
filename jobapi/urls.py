"""
URL configuration for jobapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Simple view function for the root URL
def api_root(request):
    return JsonResponse({
        "message": "Welcome to Job Portal API",
        "endpoints": {
            "admin": "/admin/",
            "api": "/api/",
            "accounts": "/api/accounts/",
            "companies": "/api/companies/",
            "jobs": "/api/jobs/",
            "test": "/api-test/"
        }
    })

# Test endpoint for POST requests
@csrf_exempt
def test_post(request):
    if request.method == 'POST':
        return JsonResponse({"message": "POST request received successfully"})
    return JsonResponse({"message": "Use POST method for this endpoint"})

# Super simple test endpoint
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def simple_test(request):
    return Response({
        "message": "API is working correctly",
        "method": request.method,
        "data_received": request.data if request.method == 'POST' else None
    })

# Token test endpoint
@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def token_test(request):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header:
        return Response({
            "message": "No Authorization header found",
            "instructions": "Add 'Authorization: Token your_token_here' to your request headers"
        })
    
    try:
        # Check if header starts with "Token "
        if not auth_header.startswith('Token '):
            return Response({
                "message": "Invalid Authorization header format",
                "correct_format": "Token your_token_here",
                "current_header": auth_header
            })
        
        # Extract token
        token_key = auth_header.split(' ')[1]
        from rest_framework.authtoken.models import Token
        token = Token.objects.filter(key=token_key).first()
        
        if not token:
            return Response({
                "message": "Invalid token",
                "token_received": token_key,
                "suggestion": "Try logging in again to get a valid token"
            })
        
        return Response({
            "message": "Token is valid",
            "user_id": token.user.id,
            "username": token.user.username,
            "user_type": token.user.user_type
        })
    except Exception as e:
        return Response({
            "message": "Error validating token",
            "error": str(e),
            "auth_header_received": auth_header
        })

urlpatterns = [
    path('', api_root, name='api_root'),  # Root URL pattern
    path('test-post/', test_post, name='test_post'),  # Test POST endpoint
    path('api-test/', simple_test, name='simple_test'),  # Direct test endpoint
    path('token-test/', token_test, name='token_test'),  # Token validation test
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/companies/', include('companies.urls')),
    path('api/', include('jobs.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

# Add media URL for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
