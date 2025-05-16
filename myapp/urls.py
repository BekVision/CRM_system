from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),


    # Customer url ________________________________
    path('customers/', views.customers_view, name='customers'),
    path('customers/<int:pk>/edit/', views.customer_update_view, name='customer_edit'),
    path('customers/<int:pk>/delete/', views.customer_delete_view, name='customer_delete'),
    path('customers/<int:pk>/orders/', views.customer_orders_view, name='customer_orders'),


    # product url ________________________________
    path('categories/', views.category_list_create, name='categories'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Product URLs
    path('products/', views.product_list_create, name='products'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # Inventory status URL
    path('products/<int:pk>/inventory/', views.product_inventory, name='product_inventory'),

    # order url ________________________________
    path('orders/', views.order_list_view, name='order_list'),
    path('orders/new/', views.order_create_view, name='order_create'),
    path('orders/<int:pk>/', views.order_detail_view, name='order_detail'),
    path('orders/<int:pk>/status/', views.order_update_status_view, name='order_update_status'),

    # Shipment url ________________________________
    path('orders/<int:order_id>/shipment/add/', views.shipment_create, name='shipment_create'),
    path('shipment/<int:shipment_id>/', views.shipment_detail, name='shipment_detail'),
    path('shipment/<int:shipment_id>/edit/', views.shipment_update, name='shipment_update'),

    # payment url ________________________________
    path('orders/<int:order_id>/payment/add/', views.payment_create, name='payment_create'),
    path('payment/<int:payment_id>/', views.payment_detail, name='payment_detail'),
    path('payment/<int:payment_id>/edit/', views.payment_update, name='payment_update'),

    # payment url ________________________________
    path('admin2/statistics/', views.admin_stats_view, name='admin_stats'),

]