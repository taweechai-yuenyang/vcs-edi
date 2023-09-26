"""
URL configuration for webbase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from django.views.generic import RedirectView
from supplier import urls as supplier_urls

from rest_framework_simplejwt import views as jv

admin.site.site_title = "EDI Web Application"
admin.site.site_header = "EDI Web Application"
admin.site.index_title = "EDI Management System"


urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path('api-auth/', include('rest_framework.urls')),
    path("api/", include(supplier_urls)),
    path('api/token/', jv.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', jv.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('tinymce/', include('tinymce.urls')),
    path("", RedirectView.as_view(url="admin/", permanent=True)),
]
