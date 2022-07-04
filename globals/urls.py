from email.policy import default
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as get_swagger_view

schema_view = get_swagger_view(
    openapi.Info(
        title='Bookit API',
        default_version='1.0.0',
        description='API documentation for online events booking application',
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1', include([
        path('', include('apps.Router')),
        path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ])),
]
