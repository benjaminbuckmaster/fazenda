from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bean-information/', views.bean_information, name='bean-information'),
    path('stock-management/', views.stock_management, name='stock-management'),
    path('stock-entry/<int:pk>', views.stock_entry, name='stock-entry'),
    path('edit-bean/<int:pk>', views.edit_bean, name='edit-bean'),
    path('logout/', views.logout_user, name='logout'),
    path('stock-offset/<int:pk>', views.stock_offset, name='stock-offset'),
]