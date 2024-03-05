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

    path('new-stock-adjustment/', views.new_stock_adjustment, name='new-stock-adjustment'),
    path('new-stock-adjustment/<int:pk>/', views.new_stock_adjustment, name='new-stock-adjustment-detail'),
    path('stock-adjustments/', views.view_stock_adjustments, name='stock-adjustments'),
    path('edit-stock-adjustment/<int:id>/', views.edit_stock_adjustment, name='edit-stock-adjustment'),

    path('edit-bean/<int:pk>', views.edit_bean, name='edit-bean'),
    path('logout/', views.logout_user, name='logout'),
    
]