from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(r'api.urls')),
    path('prompts/', include(r'prompts.urls')),
    path('users/', include(r'users.urls')),
]
