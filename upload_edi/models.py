import uuid
from django.db import models

from supplier.models import Book, ManagementUser, Product

REVISE_LEVEL = [
    ('0', 'Revise 0'),
    ('1', 'Revise 1'),
    ('2', 'Revise 2'),
    ('3', 'Revise 3'),
    ('4', 'Revise 4'),
    ('5', 'Revise 5'),
]

# Create your models here.
class UploadEDI(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    edi_file = models.FileField(upload_to='static/edi/%Y-%m-%d/', verbose_name="FILE EDI", null=False, blank=False)
    upload_seq = models.CharField(max_length=1, choices=REVISE_LEVEL, verbose_name="Upload Seq.", default="0")
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    upload_by_id = models.ForeignKey(ManagementUser, verbose_name="Upload By ID", blank=False, null=True, on_delete=models.SET_NULL)
    is_generated = models.BooleanField(verbose_name="Is Generated", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "tbtUploadFileEDI"
        verbose_name = "ข้อมูล UploadFileEDI"
        verbose_name_plural = "Upload File EDI"
        
class RequestOrder(models.Model):
    # REQUEST ORDER
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    created_by_id = models.ForeignKey(ManagementUser, verbose_name="Created By ID", blank=False, null=True, on_delete=models.SET_NULL)
    edi_file_id = models.ForeignKey(UploadEDI, verbose_name="EDI File ID", blank=False, null=False, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, verbose_name="Product ID", blank=False, null=False, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, verbose_name="Book ID", blank=False, null=True, on_delete=models.SET_NULL)
    revise_level = models.CharField(max_length=1, choices=REVISE_LEVEL, verbose_name="Revise Level", default="0")
    qty = models.FloatField(verbose_name="Qty.", default="0.0")
    is_completed = models.BooleanField(verbose_name="Generate Purchase Request", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "tbtRequestOrder"
        verbose_name = "ข้อมูล Request Order"
        verbose_name_plural = "Request Order"
        
# class PurchaseRequest(models.Model):
#     id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
#     created_by_id = models.ForeignKey(ManagementUser, verbose_name="Created By ID")
#     request_order_id = models.ForeignKey(RequestOrder, verbose_name="Request Order ID", blank=False, null=False, on_delete=models.CASCADE)
#     book_id = models.ForeignKey(Book, verbose_name="Book ID", blank=False, null=True, on_delete=models.SET_NULL)
#     purchase_no = models.CharField(verbose_name="Purchase No", max_length=50, null=False, blank=False)
#     purchase_date = models.DateField(verbose_name="Purchase Date", blank=False, null=False)
#     revise_level = models.CharField(max_length=1, choices=REVISE_LEVEL, verbose_name="Revise Level", default="0")
#     item = models.IntegerField(verbose_name="Item", default="0")
#     qty = models.FloatField(verbose_name="Qty.", default="0.0")
#     is_created_po = models.BooleanField(verbose_name="Is Created To PO", default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = "tbtPurchaseRequest"
#         verbose_name = "ข้อมูล Purchase Request"
#         verbose_name_plural = "Purchase Request"
        
# class PurchaseRequestDetail(models.Model):
#     # PURCHASE REQUEST DETAIL
#     id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
#     created_by_id = models.ForeignKey(ManagementUser, verbose_name="Created By ID")
#     purchase_request_id = models.ForeignKey(PurchaseRequest, verbose_name="Purchase Request ID", blank=False, null=False, on_delete=models.CASCADE)
#     product_id = models.ForeignKey(Product, verbose_name="Product ID", blank=False, null=False, on_delete=models.SET_NULL)
#     qty = models.FloatField(verbose_name="Qty.", default="0.0")
#     is_purchase = models.BooleanField(verbose_name="Is Purchase", default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = "tbtPurchaseOrderDetail"
#         verbose_name = "ข้อมูล Purchase Request Detail"
#         verbose_name_plural = "Purchase Request Detail"
        
# # PurchaseOrder
# class PurchaseOrder(models.Model):
#     # PURCHASE ORDER
#     id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
#     created_by_id = models.ForeignKey(ManagementUser, verbose_name="Created By ID")
#     purchase_id = models.ForeignKey(PurchaseRequest, verbose_name="Purchase ID", blank=False, null=False, on_delete=models.CASCADE)
#     book_id = models.ForeignKey(Book, verbose_name="Book ID", blank=False, null=True, on_delete=models.SET_NULL)
#     order_no = models.CharField(verbose_name="Order No", max_length=50, null=False, blank=False)
#     order_date = models.DateField(verbose_name="Order Date", blank=False, null=False)
#     item = models.IntegerField(verbose_name="Item", default="0")
#     qty = models.FloatField(verbose_name="Qty.", default="0.0")
#     is_sync = models.BooleanField(verbose_name="Is Sync", default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = "tbtPurchaseOrder"
#         verbose_name = "ข้อมูล Purchase Order"
#         verbose_name_plural = "Purchase Order"
        
# class PurchaseOrderDetail(models.Model):
#     # PURCHASE ORDER DETAIL
#     id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
#     created_by_id = models.ForeignKey(ManagementUser, verbose_name="Created By ID")
#     purchase_order_id = models.ForeignKey(PurchaseOrder, verbose_name="Purchase Order ID", blank=False, null=False, on_delete=models.CASCADE)
#     product_id = models.ForeignKey(Product, verbose_name="Product ID", blank=False, null=False, on_delete=models.SET_NULL)
#     qty = models.FloatField(verbose_name="Qty.", default="0.0")
#     is_active = models.BooleanField(verbose_name="Is Active", default=False)
#     is_sync = models.BooleanField(verbose_name="Is Sync", default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = "tbtPurchaseOrderDetail"
#         verbose_name = "ข้อมูล Purchase Order Detail"
#         verbose_name_plural = "Purchase Order Detail"