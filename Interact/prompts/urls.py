from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_prompts),
    # path('v2/', views.prompt_list_generic),
    # path('v3/', views.prompt_list_generic_v3),

    # path('<int:prompt_pk>/', views.retrieve_prompt),
    # path('<int:pk>/v2/', views.prompt_retrieve_generic),

    path('create/', views.create_prompt),
    # path('create/v2', views.prompt_create_generic),

    path('my-prompts/', views.get_proifle_prompts),
    path('<int:id>/edit/', views.update_prompt),
    # path(),
    path('<int:id>/delete/', views.delete_prompt),
    # path('<int:pk>/delete/v2/', views.prompt_delete_generic),

    # path('<int:prompt_pk>/update/',views.update_promp),
    # path('<int:pk>/update/v2/',views.prompt_update_generic),

    # path('<str:username>/prompts/', views.profile_prompts, name='profile-prompts'),
    # path('<str:username>/prompts/v2/', views.prompts_user_generic, name='profile-prompts1')

    
]