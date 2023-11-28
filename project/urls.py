"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from django.conf.urls.static import static

from api.views import main_spa  # Ensure you import main_spa correctly from your api app

urlpatterns = [
    path('', main_spa, name='main_spa'),  # Root URL to serve the main SPA
    path('health/', lambda request: HttpResponse("OK")),  # Health check URL
    path('admin/', admin.site.urls),  # URL for Django admin interface
    path('api/', include('api.urls')),  # Include URLs from your 'api' app
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

