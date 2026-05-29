from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from .views import home

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
]