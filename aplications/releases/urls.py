from django.urls import path
from . import views

urlpatterns = [
    path('', views.solicitudes_list_view, name='panel'),
    path('create/', views.create_solicitud_view, name='create_solicitud'),
    path('edit/<int:pk>/', views.edit_solicitud_view, name='edit_solicitud'),
    path('detail/<int:pk>/', views.detail_solicitud_view, name='detail_solicitud'),
    path('register/', views.register_user_view, name='register_user'),
    path('logout/', views.logout_view, name='logout'),
]
