import uuid
import django
from django.db import models
from django.utils.timezone import now
from supplier.models import Book, ManagementUser, Product, ProductGroup, Section, Supplier

REVISE_LEVEL = [
    ('0', 'Revise 0'),
    ('1', 'Revise 1'),
    ('2', 'Revise 2'),
    ('3', 'Revise 3'),
    ('4', 'Revise 4'),
    ('5', 'Revise 5'),
]

EDI_REQUEST_STATUS = [
    ('0', 'Draff'),
    ('1', 'In Process'),
    ('2', 'Success'),
]

PURCHASE_STATUS = [
    ('0', 'Draff'),
    ('1', 'Wait for Approve'),
    ('2', 'Purchase Order'),
    ('3', 'Approve'),
    ('4', 'Cancel'),
    ('5', 'Reject'),
    ('6', 'Revise')
]

PURCHASE_ORDER_STATUS = [
    ('0', 'Draff'),
    ('1', 'Wait for Approve'),
    ('2', 'Approve'),
    ('3', 'Cancel'),
    ('4', 'Reject'),
    ('5', 'Revise')
]

# Create your models here.
class UploadEDI(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    section_id = models.ForeignKey(Section, verbose_name="Section ID", blank=True,null=True, on_delete=models.SET_NULL)
    book_id = models.ForeignKey(Book, verbose_name="Book ID", blank=True,null=True, on_delete=models.SET_NULL)
    supplier_id = models.ForeignKey(Supplier, verbose_name="Supplier ID", blank=False, on_delete=models.CASCADE)
    edi_file = models.FileField(upload_to='upload_edi/static/edi/%Y-%m-%d/', verbose_name="FILE EDI", null=False, blank=False)
    edi_filename = models.CharField(max_length=150,verbose_name="FILE EDI",blank=True, null=True, editable=False, unique=True)
    document_no = models.CharField(max_length=150,verbose_name="Document No.",blank=True, null=True, editable=False)
    upload_date = models.DateField(verbose_name="Upload On",default=django.utils.timezone.now)
    upload_seq = models.CharField(max_length=1, choices=REVISE_LEVEL, verbose_name="Revise Level", default="0")
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    upload_by_id = models.ForeignKey(ManagementUser, verbose_name="Upload By ID", blank=True, null=True, on_delete=models.SET_NULL, editable=False)
    is_generated = models.BooleanField(verbose_name="Is Generated", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.document_no
    
    class Meta:
        db_table = "ediFileUpload"
        verbose_name = "UploadFileEDI"
        verbose_name_plural = "Upload File EDI"
        
class RequestOrder(models.Model):
    # REQUEST ORDER
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    edi_file_id = models.ForeignKey(UploadEDI, verbose_name="EDI File ID", blank=False, null=False, on_delete=models.CASCADE, editable=False)
    supplier_id = models.ForeignKey(Supplier, verbose_name="Supplier ID", on_delete=models.SET_NULL, null=True, blank=True)
    section_id = models.ForeignKey(Section, verbose_name="Section ID", blank=True,null=True, on_delete=models.SET_NULL)
    product_group_id = models.ForeignKey(ProductGroup, verbose_name="Model ID", on_delete=models.SET_NULL, null=True, blank=True)
    book_id = models.ForeignKey(Book, verbose_name="Book ID", blank=True,null=True, on_delete=models.SET_NULL)
    ro_no = models.CharField(max_length=50,verbose_name="Request No.", blank=True, null=True)
    ro_date = models.DateField(verbose_name="Request Date",  null=True, blank=True)
    ro_item = models.IntegerField(verbose_name="Item", blank=True,null=True, default="0")
    ro_qty = models.FloatField(verbose_name="Qty.", blank=True,null=True, default="0")
    ro_by_id = models.ForeignKey(ManagementUser, verbose_name="Request By ID", blank=True, null=True, on_delete=models.SET_NULL)
    ro_status = models.CharField(max_length=1, choices=EDI_REQUEST_STATUS,verbose_name="Request Status", default="0")
    is_sync = models.BooleanField(verbose_name="Is Sync", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = "ediRO"
        verbose_name = "Request Order"
        verbose_name_plural = "Request Order"
        ordering = ('ro_date','ro_no')
        
class RequestOrderDetail(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    request_order_id = models.ForeignKey(RequestOrder, verbose_name="Request ID", blank=False, null=False, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, verbose_name="Product ID", blank=False, null=False, on_delete=models.CASCADE)
    request_qty = models.FloatField(verbose_name="Request Qty.", default="0.0")
    balance_qty = models.FloatField(verbose_name="Balance Qty.", default="0.0")
    request_by_id = models.ForeignKey(ManagementUser, verbose_name="Request By ID", blank=True, null=True, on_delete=models.SET_NULL)
    request_status = models.CharField(max_length=1, choices=EDI_REQUEST_STATUS,verbose_name="Request Status", default="0")
    is_selected = models.BooleanField(verbose_name="Is Selected", default=True)
    is_sync = models.BooleanField(verbose_name="Is Sync", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.product_id
    
    def __str__(self):
        return self.product_id
    
    class Meta:
        db_table = "ediRODetail"
        verbose_name = "Request Order Detail"
        verbose_name_plural = "Request Order Detail"
        ordering = ('product_id','created_at','updated_at')
        

        
class ApproveRequestOrder(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    request_order_id = models.ForeignKey(RequestOrder, verbose_name="Request ID", blank=False, null=False, on_delete=models.CASCADE)
    request_by_id = models.ForeignKey(ManagementUser, verbose_name="Request By ID", blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    request_status = models.CharField(max_length=1, choices=EDI_REQUEST_STATUS,verbose_name="Request Status", default="0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "ediROApprove"
        verbose_name = "Approve Request Order"
        verbose_name_plural = "Approve Request Order"
        
# เปิด PR
class PurchaseRequest(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    edi_file_id = models.ForeignKey(UploadEDI, verbose_name="EDI File ID", blank=False, null=True, on_delete=models.SET_NULL)
    section_id = models.ForeignKey(Section, verbose_name="Section ID", on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, verbose_name="Book ID", on_delete=models.CASCADE)
    supplier_id = models.ForeignKey(Supplier, verbose_name="Supplier ID", on_delete=models.CASCADE)
    purchase_no = models.CharField(verbose_name="Purchase No", max_length=50, null=False, blank=False)
    purchase_date = models.DateField(verbose_name="Purchase Date", blank=False, null=False)
    revise_level = models.CharField(max_length=1, choices=REVISE_LEVEL, verbose_name="Revise Level", default="0")
    item = models.IntegerField(verbose_name="Item", default="0")
    qty = models.FloatField(verbose_name="Qty.", default="0.0")
    description = models.TextField(verbose_name="Description", default="-", blank=True, null=True)
    created_by_id = models.ForeignKey(ManagementUser, verbose_name="Created By ID", null=True, blank=True, on_delete=models.SET_NULL)
    ref_no = models.CharField(verbose_name="Ref No", max_length=8, blank=True, null=True)
    purchase_status = models.CharField(max_length=1,verbose_name="Purchase Status", choices=PURCHASE_STATUS, default="0", null=True, blank=True)
    is_sync = models.BooleanField(verbose_name="Status Sync", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.purchase_no
    
    class Meta:
        db_table = "ediPR"
        verbose_name = "Purchase Request"
        verbose_name_plural = "Purchase Request"
        
class PurchaseRequestDetail(models.Model):
    # PURCHASE REQUEST DETAIL
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    purchase_request_id = models.ForeignKey(PurchaseRequest, verbose_name="Purchase Request ID", blank=False, null=False, on_delete=models.CASCADE)
    request_order_id = models.ForeignKey(RequestOrder, verbose_name="Request Order ID", blank=True, null=True, on_delete=models.SET_NULL)
    product_group_id = models.ForeignKey(ProductGroup, verbose_name="Model ID", on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, verbose_name="Product ID", blank=False, null=False, on_delete=models.CASCADE)
    seq = models.IntegerField(verbose_name="Sequence", blank=True, null=True,default="0")
    qty = models.FloatField(verbose_name="Qty.", default="0.0")
    is_confirm = models.BooleanField(verbose_name="Confirmed", default=False)
    is_sync = models.BooleanField(verbose_name="Status Sync", default=False)
    created_by_id = models.ForeignKey(ManagementUser, verbose_name="Created By ID", blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "ediPRDetail"
        verbose_name = "Purchase Request Detail"
        verbose_name_plural = "Purchase Request Detail"
        ordering = ['purchase_request_id','seq']
        
class ApprovePurchaseRequest(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    request_order_id = models.ForeignKey(PurchaseRequest, verbose_name="Purchase Request ID", blank=False, null=False, on_delete=models.CASCADE)
    approve_by_id = models.ForeignKey(ManagementUser, verbose_name="Approve By ID", blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    purchase_request_status = models.CharField(max_length=1, choices=PURCHASE_STATUS,verbose_name="Purchase Request Status", default="0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "ediPRApprove"
        verbose_name = "Approve Purchase Request"
        verbose_name_plural = "Approve Purchase Request"
        
# # PurchaseOrder
class PurchaseOrder(models.Model):
    # PURCHASE ORDER
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    purchase_id = models.ForeignKey(PurchaseRequest, verbose_name="Purchase ID", blank=False, null=False, on_delete=models.CASCADE)
    order_no = models.CharField(verbose_name="Order No", max_length=50, null=False, blank=False)
    order_date = models.DateField(verbose_name="Order Date", blank=False, null=False)
    item = models.IntegerField(verbose_name="Item", default="0")
    qty = models.FloatField(verbose_name="Qty.", default="0.0")
    order_status = models.CharField(max_length=1, verbose_name="Order Status", default="0")
    description = models.TextField(verbose_name="Description", default="-", blank=True, null=True)
    ref_no = models.CharField(verbose_name="Ref No", max_length=8, blank=True, null=True)
    is_sync = models.BooleanField(verbose_name="Is Sync", default=False)
    created_by_id = models.ForeignKey(ManagementUser, verbose_name="Created By ID", blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "ediPO"
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Order"
        
class PurchaseOrderDetail(models.Model):
    # PURCHASE ORDER DETAIL
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    purchase_order_id = models.ForeignKey(PurchaseOrder, verbose_name="Purchase Order ID", blank=False, null=False, on_delete=models.CASCADE)
    product_group_id = models.ForeignKey(ProductGroup, verbose_name="Model ID", on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, verbose_name="Product ID", blank=False, null=False, on_delete=models.CASCADE)
    qty = models.FloatField(verbose_name="Qty.", default="0.0")
    is_active = models.BooleanField(verbose_name="Is Active", default=False)
    is_sync = models.BooleanField(verbose_name="Is Sync", default=False)
    created_by_id = models.ForeignKey(ManagementUser, verbose_name="Created By ID", blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "ediPODetail"
        verbose_name = "Purchase Order Detail"
        verbose_name_plural = "Purchase Order Detail"
        
class ApprovePurchaseOrder(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    purchase_order_id = models.ForeignKey(PurchaseOrder, verbose_name="Purchase Request ID", blank=False, null=False, on_delete=models.CASCADE)
    approve_by_id = models.ForeignKey(ManagementUser, verbose_name="Approve By ID", blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    purchase_request_status = models.CharField(max_length=1, choices=PURCHASE_ORDER_STATUS, verbose_name="Purchase Order Status", default="0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "ediPOApprove"
        verbose_name = "Approve Purchase Order"
        verbose_name_plural = "Approve Purchase Order"