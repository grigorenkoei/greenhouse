from . import views
from django.urls import path

# It's for relative urls
app_name = 'basic_app'

urlpatterns = [
    path('find_client/', views.find_client, name='find_client'),
    path('add_client/', views.add_client, name='add_client'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    #   path('discount_setup/', views.discount_setup, name='discount_setup'),
    path('add_flat/', views.add_flat, name='add_flat'),
    path('flats/', views.flats, name='flats'),
    path('success/', views.success, name='success'),
    path('delete_order/<int:id>', views.delete_order, name='delete_order'),
    path('delete_flat/<int:id>', views.delete_flat, name='delete_flat'),
]
