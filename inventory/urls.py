from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bean-information/', views.bean_information, name='bean-information'),
    path('stock-management/', views.stock_management, name='stock-management'),
    
    path('new-stock-entry/', views.new_stock_entry, name='new-stock-entry'),
    path('new-stock-entry/<int:pk>/', views.new_stock_entry, name='new-stock-entry-detail'),
    path('stock-entries/', views.view_stock_entries, name='stock-entries'),
    path('stock-entries/<int:pk>/', views.view_stock_entries, name='stock-entries-detail'),
    path('edit-stock-entry/<int:id>/', views.edit_stock_entry, name='edit-stock-entry'),

    path('edit-bean/<int:pk>', views.edit_bean, name='edit-bean'),
    path('logout/', views.logout_user, name='logout'),
    path('stock-offset/<int:pk>/', views.stock_offset, name='stock-offset'),
]