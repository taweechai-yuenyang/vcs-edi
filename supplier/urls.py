from django.urls import include, path
from rest_framework import routers

from . import views

urlpatterns = [
    path('supplier', views.SupplierListApiView.as_view()),
    path('order_type', views.OrderTypeListApiView.as_view()),
    path('product_type', views.ProductTypeListApiView.as_view()),
    path('unit', views.UnitListApiView.as_view()),
    path('product', views.ProductListApiView.as_view()),
]