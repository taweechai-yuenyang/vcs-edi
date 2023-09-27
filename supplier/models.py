import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    user_id = models.ManyToManyField(User, blank=True, verbose_name="User ID",null=True)
    skid = models.CharField(max_length=8, verbose_name="Formula ID", unique=True, blank=False, null=False)
    code = models.CharField(max_length=150, verbose_name="Code", unique=True, blank=False, null=False)
    name = models.CharField(max_length=150, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description", blank=True, default="-")
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        # db_table_comment = "formula_vcst"
        # app_label = "budgetaaa"
        # ordering = ('-updated_on','code','name')
        db_table = "tbmSupplier"
        verbose_name = "ข้อมูล Supplier"
        verbose_name_plural = "Supplier"
        
class OrderType(models.Model):
    # select p.FCSKID,p.FCCODE,p.FCNAME,p.FCNAME2 from PRODTYPE p
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    code = models.CharField(max_length=50, verbose_name="Code", unique=True, blank=False, null=False)
    name = models.CharField(max_length=150, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description", blank=True, default="-")
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmOrderType"
        verbose_name = "ข้อมูล Order Type"
        verbose_name_plural = "Order Type"
        
class ProductType(models.Model):
    # select p.FCCODE,p.FCNAME,p.FCNAME2 from PRODTYPE p
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    code = models.CharField(max_length=50, verbose_name="Code", unique=True, blank=False, null=False)
    name = models.CharField(max_length=150, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description", blank=True, default="-")
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmProductType"
        verbose_name = "ข้อมูล Product Type"
        verbose_name_plural = "Product Type"
        
class Unit(models.Model):
    # select p.FCSKID,p.FCCODE,p.FCNAME,p.FCNAME2 from UM p
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    code = models.CharField(max_length=50, verbose_name="Code", unique=True,blank=False, null=False)
    name = models.CharField(max_length=150, verbose_name="Name", unique=True,blank=False, null=False)
    description = models.TextField(verbose_name="Description", blank=True, default="-")
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmUnit"
        verbose_name = "ข้อมูล Unit"
        verbose_name_plural = "Unit"
        
class Product(models.Model):
    # select p.FCSKID,p.FCTYPE,p.FCCODE,p.FCNAME,p.FCNAME2 from PROD p
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    skid = models.CharField(max_length=8, verbose_name="Formula ID", unique=True, blank=False, null=False)
    prod_type_id = models.ForeignKey(ProductType, blank=True, verbose_name="Product Type ID", on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=50, verbose_name="Code", blank=False, null=False)
    name = models.CharField(max_length=150, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description", blank=True, default="-")
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmProduct"
        verbose_name = "ข้อมูล Product"
        verbose_name_plural = "Product"