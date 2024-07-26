from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bean-information/', views.bean_information, name='bean-information'),
    path('stock-management/', views.stock_management, name='stock-management'),
    
    path('new-stock-entry/', views.new_stock_entry, name='new-stock-entry'),
    path('new-stock-entry/<int:pk>/', views.new_stock_entry, name='new-stock-entry-detail'),
    # path('stock-entries/', views.view_stock_entries, name='stock-entries'),
    path('stock-entries/<int:pk>/', views.view_stock_entries, name='stock-entries-detail'),
    path('edit-stock-entry/<int:id>/', views.edit_stock_entry, name='edit-stock-entry'),

    path('new-stock-adjustment/', views.new_stock_adjustment, name='new-stock-adjustment'),
    path('new-stock-adjustment/<int:pk>/', views.new_stock_adjustment, name='new-stock-adjustment-detail'),
    path('stock-adjustments/', views.view_stock_adjustments, name='stock-adjustments'),
    path('stock-adjustments/<int:pk>/', views.view_stock_adjustments, name='stock-adjustments-detail'),
    path('edit-stock-adjustment/<int:id>/', views.edit_stock_adjustment, name='edit-stock-adjustment'),

    path('statistics/', views.statistics, name='statistics'),
    path('stock-use-over-time/', views.stock_use_over_time, name='stock-use-over-time'),
    path('stock-use-per-month/', views.stock_use_per_month, name='stock-use-per-month'),
    path('consumption-30-days/', views.consumption_30_days, name='consumption-30-days'),

    path('bean-details/<int:pk>', views.bean_details, name='bean-details'),
    path('logout/', views.logout_user, name='logout'),


    
]