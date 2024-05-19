from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("allauth.urls")),
    path('accounts/', include('allauth.socialaccount.urls')),
    path('', include('main.urls')),
    re_path('task/', include('task.urls')),
]
