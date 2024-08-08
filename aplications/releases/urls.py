from django.urls import path
from . import views

urlpatterns = [
    path('', views.solicitudes_list_view, name='panel'),  # Vista principal de las solicitudes
    path('create/', views.create_solicitud_view, name='create_solicitud'),  # Vista para crear solicitudes
    path('edit/<int:pk>/', views.edit_solicitud_view, name='edit_solicitud'),  # Vista para editar solicitudes
    path('register/', views.register_user_view, name='register_user'),  # Vista para registrar usuarios
    path('logout/', views.logout_view, name='logout'),  # Vista para cerrar sesión
]
