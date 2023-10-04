import uuid
from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
class OrderType(models.Model):
    # select p.FCSKID,p.FCCODE,p.FCNAME,p.FCNAME2 from PRODTYPE p
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    code = models.CharField(max_length=50, verbose_name="Code", unique=True, blank=False, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmOrderType"
        verbose_name = "Order Type"
        verbose_name_plural = "Order Type"
        
class ProductType(models.Model):
    # select p.FCCODE,p.FCNAME,p.FCNAME2 from PRODTYPE p
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    code = models.CharField(max_length=50, verbose_name="Code", unique=True, blank=False, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmProductType"
        verbose_name = "Product Type"
        verbose_name_plural = "Product Type"
        
class ProductGroup(models.Model):
    # select FCSKID,FCCODE,FCNAME,FCNAME2 from PDGRP
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    code = models.CharField(max_length=50, verbose_name="Code", unique=True,blank=False, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmProductGroup"
        verbose_name = "Product Group"
        verbose_name_plural = "Product Group"
        
class Unit(models.Model):
    # select p.FCSKID,p.FCCODE,p.FCNAME,p.FCNAME2 from UM p
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    code = models.CharField(max_length=50, verbose_name="Code", unique=True,blank=False, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmUnit"
        verbose_name = "Unit"
        verbose_name_plural = "Unit"
        
class Section(models.Model):
    # select FCSKID,FCCODE,FCNAME,FCNAME2 from SECT
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    code = models.CharField(max_length=50, verbose_name="Code", unique=True,blank=False, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmSection"
        verbose_name = "Section"
        verbose_name_plural = "Section"
        
class Position(models.Model):
    # select FCSKID,FCCODE,FCNAME,FCNAME2 from SECT
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    code = models.CharField(max_length=50, verbose_name="Code", unique=True,blank=False, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmPosition"
        verbose_name = "Position"
        verbose_name_plural = "Position"

class Department(models.Model):
    # select FCSKID,FCCODE,FCNAME,FCNAME2 from DEPT
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    code = models.CharField(max_length=50, verbose_name="Code", unique=True,blank=False, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmDepartment"
        verbose_name = "Department"
        verbose_name_plural = "Department"
        
        
class Book(models.Model):
    # select FCSKID,FCREFTYPE,FCCODE,FCNAME,FCNAME2,FCPREFIX from BOOK
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    skid = models.CharField(max_length=50, verbose_name="Key", unique=True, blank=False, null=False)
    order_type_id = models.ForeignKey(OrderType, verbose_name="Type ID", on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=50, verbose_name="Code", blank=False, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", blank=False, null=False)
    prefix = models.CharField(max_length=250, verbose_name="Prefix", blank=True, null=True)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code}-{self.name}"
    
    class Meta:
        db_table = "tbmBook"
        verbose_name = "Book"
        verbose_name_plural = "Book"
        
class Product(models.Model):
    # select p.FCSKID,p.FCTYPE,g.FCCODE,p.FCCODE,p.FCNAME,p.FCNAME2 from PROD p inner join PDGRP g on p.FCPDGRP=g.FCSKID where p.FCTYPE in ('1','5') order by p.FCCODE 
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    prod_type_id = models.ForeignKey(ProductType, verbose_name="Product Type ID", on_delete=models.SET_NULL, null=True)
    prod_group_id = models.ForeignKey(ProductGroup, verbose_name="Product Group ID", on_delete=models.SET_NULL, null=True)
    unit_id = models.ForeignKey(Unit, verbose_name="Unit ID", on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=150, verbose_name="Code", unique=True, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    img = models.ImageField(verbose_name="Image")
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmProduct"
        verbose_name = "Product"
        verbose_name_plural = "Product"
        
class ManagementUser(AbstractUser):
    formula_user_id = models.CharField(max_length=8, verbose_name="Formula User ID", blank=True, null=True)
    department_id = models.ForeignKey(Department, blank=True, verbose_name="Department ID",null=True, on_delete=models.SET_NULL)
    position_id = models.ForeignKey(Position, blank=True, verbose_name="Position ID",null=True, on_delete=models.SET_NULL)
    section_id = models.ForeignKey(Section, blank=True, verbose_name="Section ID",null=True, on_delete=models.SET_NULL)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    avatar_url = models.ImageField(verbose_name="Avatar Image",blank=True, null=True)
    signature_img = models.ImageField(verbose_name="Signature Image",blank=True, null=True)
    is_approve = models.BooleanField(verbose_name="Is Approve", default=False)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return super().__str__()
    
    class Meta:
        # db_table_comment = "formula_vcst"
        # app_label = "budgetaaa"
        # ordering = ('-updated_on','code','name')
        db_table = "ediUser"
        verbose_name = "User"
        verbose_name_plural = "User"
    
class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    user_id = models.ManyToManyField(ManagementUser, blank=True, verbose_name="User ID",null=True)
    # skid = models.CharField(max_length=8, verbose_name="Formula ID", unique=True)
    code = models.CharField(max_length=150, verbose_name="Code",unique=True,blank=False, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
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
        verbose_name = "Supplier"
        verbose_name_plural = "Supplier"