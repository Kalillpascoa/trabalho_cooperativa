from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('grappelli/', include('grappelli.urls')),

    path('admin/', admin.site.urls),

    path('', include('plataforma.urls')),
]