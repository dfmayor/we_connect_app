from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('add_category/', views.add_category, name='add_category'),
    path('list_category/', views.list_category, name='list_category'),
    path('create_service/', views.create_service, name='create_service'),
    path('get_services/', views.get_home_services, name='get_services'),
    path('service_details/<uuid:id>/', views.service_details, name='service_details'),
    path('add_review/', views.add_review, name='add_review'),
    path('request_service/', views.request_service, name='request_service'),
]