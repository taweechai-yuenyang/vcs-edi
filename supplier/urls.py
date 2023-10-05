from django.urls import include, path
from rest_framework import routers

from . import views

urlpatterns = [
    path('supplier', views.SupplierListApiView.as_view()),
    path('order_type', views.OrderTypeListApiView.as_view()),
    path('product_type', views.ProductTypeListApiView.as_view()),
    path('unit', views.UnitListApiView.as_view()),
    path('product', views.ProductListApiView.as_view()),
    path("product_group", views.ProductGroupListApiView.as_view()),
    path("section", views.SectionListApiView.as_view()),
    path("position", views.PositionListApiView.as_view()),
    path("department", views.DepartmentListApiView.as_view()),
    path("book", views.BookListApiView.as_view()),
    path("employee", views.EmployeeListApiView.as_view()),
]