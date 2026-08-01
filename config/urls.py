"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('workouts.urls')),
    path('api-auth/', include('rest_framework.urls')),  # login/logout navegable para pruebas
    path('api/token/', obtain_auth_token),  # POST username/password, recibe un token

    # Documentación de la API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'), # OpenAPI crudo (JSON/YAML)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), # Interfaz Swagger navegable (Documentación interactiva para probar endpoints)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), # Interfaz Redoc (para leer)
]
