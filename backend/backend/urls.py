"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from airplane_manufacturing_application.views import readme_view

schema_view = get_schema_view(
   openapi.Info(
        title="Airplane Manufacturing Application API",
        default_version='v1',
        description="API documentation for Airplane Manufacturing Application (@srnahmet)",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="srnahmet98@gmail.com"),
        license=openapi.License(name="MIT License"),
   ),
   public=True,
#    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', readme_view, name='main-page'),
    path('admin/', admin.site.urls),
    path('api/', include('airplane_manufacturing_application.urls')), 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('health_check/', include('health_check.urls')),
]
