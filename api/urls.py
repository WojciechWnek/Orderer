from django.urls import path
from . import views

urlpatterns = [
    path('function-products/info/', views.product_info),

    # DFR class based view
    path('products/', views.ProductListAPIView.as_view()),
    path('products/<int:product_id>/', views.ProductDetailAPIView.as_view()),
    path('orders/', views.OrderListAPIView.as_view()),
    path('user-orders/', views.UserOrderListAPIView.as_view()),

]
