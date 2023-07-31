from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('dashboard/<str:id>/', views.dashboard, name='dashboard'),
    path('signup', views.signup_view, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('groups/', views.group_list, name='group_list'),
    path('groups/<str:group_name>/', views.view_group_users, name='group_users'),
    path('new_group/', views.add_group, name='new_group'),
    path('user_profile/', views.create_user_profile, name='user_profile'),
    path('view_profile/', views.view_user_profile, name='view_profile'),
    path('others_profile/<uuid:id>/', views.view_others_profile, name='others_profile'),
    path('all_users/', views.list_all_users, name='all_users'),
    path('save_education/', views.add_user_education, name='save_education'),
]