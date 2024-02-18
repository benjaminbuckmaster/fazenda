from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bean-information/', views.bean_information, name='bean-information'),
    path('stock-management/', views.stock_management, name='stock-management'),
    
    # Use a question mark to make the 'pk' parameter optional
    path('stock-entry/', views.stock_entry, name='stock-entry'),
    path('stock-entry/<int:pk>/', views.stock_entry, name='stock-entry-detail'),

    path('edit-bean/<int:pk>', views.edit_bean, name='edit-bean'),
    path('logout/', views.logout_user, name='logout'),
    path('stock-offset/<int:pk>/', views.stock_offset, name='stock-offset'),
]