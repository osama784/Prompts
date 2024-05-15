from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views


urlpatterns = [ 
    path('auth/', obtain_auth_token),
    path('auth/v2/', views.obtain_token),

    path('', views.list_profile_generic),

    path('create-profile/', views.create_profile),
    path('delete-profile/<str:username>/', views.delete_profile_generic),

    path('<str:username>/', views.retrieve_profile_generic),
    
]