from rest_framework import serializers
from .models import Supplier, OrderType, ProductType, Product, Unit


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('id','user_id','skid','code','name','description','is_active','created_on','updated_on',)
        
class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderType
        fields = ('id','code','name','description','is_active','created_on','updated_on',)
        
class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ('id','code','name','description','is_active','created_on','updated_on',)
        
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id','code','name','description','is_active','created_on','updated_on',)
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','skid','prod_type_id','code','name','description','is_active','created_on','updated_on',)
