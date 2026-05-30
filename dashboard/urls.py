from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('orders/', views.orders_list, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('categories/', views.categories_list, name='categories'),
    path('categories/add/', views.category_form, name='add_category'),
    path('categories/<int:category_id>/edit/', views.category_form, name='edit_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('menu-items/', views.menu_items_list, name='menu_items'),
    path('menu-items/add/', views.menu_item_form, name='add_menu_item'),
    path('menu-items/<int:item_id>/edit/', views.menu_item_form, name='edit_menu_item'),
    path('menu-items/<int:item_id>/delete/', views.delete_menu_item, name='delete_menu_item'),
    path('users/', views.users_list, name='users'),
    path('reports/', views.reports, name='reports'),
    path('search/', views.search, name='search'),
    path('analytics/', views.analytics_data, name='analytics_data'),
]
