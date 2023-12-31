from rest_framework import serializers
from .models import Book, Corporation, Department, Employee, Factory, Position, ProductGroup, Section, Supplier, RefType, ProductType, Product, Unit


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('id','user_id','code','name','description','is_active','created_on','updated_on',)
        
class RefTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefType
        fields = ('id','code','name','description','is_active','created_on','updated_on',)
        
class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ('id','code','name','description','is_active','created_on','updated_on',)

class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = ('id','code','name','description','is_active','created_on','updated_on',)
        
class CorporationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporation
        fields = ('id','code','name','description','is_active','created_on','updated_on',)
        
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id','code','name','description','is_active','created_on','updated_on',)
        
class FactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Factory
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
        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id','corporation_id','code','name','description','is_active','created_on','updated_on',)
        
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id','skid', 'corporation_id', 'order_type_id','code','name','prefix','description','is_active','created_on','updated_on',)
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','prod_type_id','prod_group_id','unit_id','code','name','description','is_active','created_on','updated_on',)
