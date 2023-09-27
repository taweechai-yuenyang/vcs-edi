import uuid
from django.db import models
from django.contrib.auth.models import User
from supplier.models import Supplier, OrderType, Product, Unit

# Create your models here.
# select o.FCSKID,o.FCCOOR,o.FCREFTYPE,o.FDDATE,o.FCCODE,o.FCREFNO,o.FNAMT,o.FCSTEP from ORDERH o where o.FCREFTYPE='PO' and o.FCSTEP='1' order by o.FDDATE 
ORDER_STEP = [
    ('N', 'None'),
    ('I', 'In Process'),
    ('P', 'Paid'),
    ('C', 'Cancel'),
    ('F', 'Finish'),
]

class OrderHead(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    order_skid = models.CharField(max_length=8, verbose_name="Formula ID", unique=True, blank=False, null=False)
    supplier_id = models.ForeignKey(Supplier, verbose_name="Supplier ID", on_delete=models.SET_NULL, null=True)
    order_type_id = models.ForeignKey(OrderType, verbose_name="Order Type ID", on_delete=models.SET_NULL, null=True)
    order_date = models.DateField(verbose_name="Order Date", blank=False, null=False)
    order_code = models.CharField(max_length=150, verbose_name="Code", unique=True, blank=False, null=False)
    order_no = models.CharField(max_length=150, verbose_name="Order No.", blank=False, null=False)
    order_amount = models.FloatField(max_length=18, verbose_name="Order Amount", default="0.0", blank=False, null=False)
    order_step = models.CharField(choices=ORDER_STEP,max_length=1, verbose_name="Order Step", default="N", blank=False)
    invoice_no = models.CharField(max_length=150, verbose_name="Invoice No.", blank=False, null=True)
    delivery_date = models.DateField(verbose_name="Delivery Date", blank=False, null=True)
    is_confirm = models.BooleanField(verbose_name="Is Confirm", default=False)
    is_sync = models.BooleanField(verbose_name="Is Sync", default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.order_no
    
    class Meta:
        db_table = "tbtOrderHead"
        verbose_name = "ข้อมูล Order"
        verbose_name_plural = "Order"
        
class OrderDetail(models.Model):
    # select i.FCSKID,i.FCORDERH,i.FCPROD,i.FNUMQTY,i.FNQTY,i.FNPRICE,i.FNVATAMT,i.FCSEQ,i.FCUM  from ORDERI i
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    order_skid = models.CharField(max_length=8, verbose_name="Formula ID", unique=True, blank=False, null=False)
    order_id = models.ForeignKey(OrderHead, verbose_name="Order ID", on_delete=models.CASCADE, null=True)
    product_id = models.ForeignKey(Product, verbose_name="Product ID", on_delete=models.CASCADE, null=True)
    unit_id = models.ForeignKey(Unit, verbose_name="Unit ID", on_delete=models.SET_NULL, null=True)
    num_qty = models.FloatField(max_length=18, verbose_name="Num Qty.", default="0.0", blank=False, null=False)
    qty = models.FloatField(max_length=18, verbose_name="Qty.", default="0.0", blank=False, null=False)
    price = models.FloatField(max_length=18, verbose_name="Price", default="0.0", blank=False, null=False)
    vat = models.FloatField(max_length=18, verbose_name="Vat.", default="0.0", blank=False, null=False)
    seq = models.IntegerField(verbose_name="Seq.", default="0", blank=False, null=False)
    confirm_qty = models.FloatField(max_length=18, verbose_name="Confirm Qty.", default="0.0", blank=False, null=False)
    order_step = models.CharField(choices=ORDER_STEP,max_length=1, verbose_name="Order Step", default="1", null=False, blank=False)
    is_confirm = models.BooleanField(verbose_name="Is Confirm", default=False)
    is_sync = models.BooleanField(verbose_name="Is Sync", default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.product_id
    
    class Meta:
        db_table = "tbtOrderDetail"
        verbose_name = "ข้อมูล Order Detail"
        verbose_name_plural = "Order Detail"
    
class OrderConfirm(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    order_detail_id = models.ForeignKey(OrderDetail, verbose_name="Order Detail ID", on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(User, verbose_name="Order Detail ID", on_delete=models.CASCADE, null=True)
    invoice_no = models.CharField(max_length=150, verbose_name="Invoice No.", blank=False, null=True)
    qty = models.FloatField(max_length=18, verbose_name="Qty.", default="0.0", blank=False, null=False)
    confirm_qty = models.FloatField(max_length=18, verbose_name="Confirm Qty.", default="0.0", blank=False, null=False)
    description = models.TextField(verbose_name="Description")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user_id}-{self.order_detail_id}"
    
    class Meta:
        db_table = "tbtOrderConfirm"
        verbose_name = "ข้อมูล Order Confirm"
        verbose_name_plural = "Order Confirm"