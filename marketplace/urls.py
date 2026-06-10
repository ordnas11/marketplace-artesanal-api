from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import home


# CONFIGURAÇÃO DO SWAGGER
schema_view = get_schema_view(
    openapi.Info(
        title="Marketplace Artesanal API",
        default_version='v1',
        description="Documentação da API Marketplace Artesanal",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    # ROTA PRINCIPAL
    path('', home),

    # ADMIN
    path('admin/', admin.site.urls),

    # APIS
    path('api/', include('core.urls')),
    path('api/', include('produtos.urls')),

    # JWT
    path(
        'api/login/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    # SWAGGER
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),

    # REDOC
    re_path(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]