from rest_framework import serializers
from .models import Book, Department, Position, ProductGroup, Section, Supplier, OrderType, ProductType, Product, Unit


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('id','user_id','code','name','description','is_active','created_on','updated_on',)
        
class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderType
        fields = ('id','code','name','description','is_active','created_on','updated_on',)
        
class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ('id','code','name','description','is_active','created_on','updated_on',)

class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = ('id','code','name','description','is_active','created_on','updated_on',)
        
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id','code','name','description','is_active','created_on','updated_on',)
        
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id','code','name','description','is_active','created_on','updated_on',)
        
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id','code','name','description','is_active','created_on','updated_on',)
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id','code','name','description','is_active','created_on','updated_on',)
        
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id','skid','order_type_id','code','name','prefix','description','is_active','created_on','updated_on',)
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','prod_type_id','prod_group_id','code','name','description','is_active','created_on','updated_on',)
