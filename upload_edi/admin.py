from io import BytesIO
from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.utils.html import format_html
import pandas as pd

from supplier.models import Book, OrderType, Product, ProductGroup
from .models import EDI_REQUEST_STATUS, PurchaseOrder, PurchaseRequest, PurchaseRequestDetail, RequestOrder, RequestOrderDetail, UploadEDI
# from .models import UploadEDI, PurchaseRequest, PurchaseOrder, RequestOrder

# Register your models here.


@admin.action(description="Mark selected as Purchase Request")
def make_request_request(modeladmin, request, queryset):
    queryset.update(status="p")


class UploadEDIAdmin(admin.ModelAdmin):
    # fields = ('section_id', 'book_id', 'supplier_id', 'product_group_id','edi_file','upload_date','upload_seq','description',)
    actions = [make_request_request]

    list_filter = ['is_generated', 'document_no', 'edi_filename', 'upload_seq']

    list_display = ('document_no', 'upload_seq', 'edi_filename', 'uploaded_at',
                    'upload_by_id', 'is_generated', 'created_on', 'updated_on')
    fieldsets = (
        (
            None, {
                "classes": ["wide", "extrapretty"],
                'fields': [
                    ('upload_date', 'upload_seq'),
                    'supplier_id', 'edi_file', 'description',
                ]}
        ),
    )

    # Set Overrides Message
    def message_user(self, request, message, level=messages.INFO, extra_tags='', fail_silently=False):
        pass

    # Default Book PR-0002
    def save_model(self, request, obj, form, change):
        if request.user.section_id:
            obj.edi_filename = obj.edi_file.name
            # Set Section From User
            obj.section_id = request.user.section_id
            # Set Book From Default
            ordType = OrderType.objects.get(code=r"PR")
            book = Book.objects.get(order_type_id=ordType, code=r'0002')
            obj.book_id = book
            # Set upload_by_id
            obj.upload_by_id = request.user
            # Generate Document No
            docNo = f"EDI{str(obj.upload_date.strftime('%Y%m%d'))[3:]}"
            n = UploadEDI.objects.filter(document_no__gte={docNo}).count()
            documentNo = f"{docNo}{(n + 1):05d}"
            obj.document_no = documentNo
            # Read Excel
            file_in_memory = request.FILES['edi_file'].read()
            data = pd.read_excel(BytesIO(file_in_memory)).to_numpy()
            addData = []
            for r in data:
                if float(r[5]) > 0:
                    partID = Product.objects.get(code=str(r[3]).strip())
                    addData.append({"partName": partID, "group_id": partID.prod_group_id,"qty": r[5]})
                    
            # show Message
            try:
                super().save_model(request, obj, form, change)
                for r in addData:
                    ### Filter Request Order Header
                    ordID = None
                    try:
                        ordID = RequestOrder.objects.get(supplier_id=obj.supplier_id,section_id=request.user.section_id,product_group_id=r["group_id"],book_id=obj.book_id,ro_date=obj.upload_date)
                    except Exception as e:
                        rndNo = f"RO{str(obj.upload_date.strftime('%Y%m%d'))[3:]}"
                        rnd = f"{rndNo}{(RequestOrder.objects.filter(ro_no__gte=rndNo).count() + 1):05d}"
                        ordID = RequestOrder(
                            edi_file_id=obj,
                            supplier_id=obj.supplier_id,
                            section_id=request.user.section_id,
                            product_group_id=r["group_id"],
                            book_id=obj.book_id,
                            ro_no=rnd,
                            ro_date=obj.upload_date,
                            ro_by_id=request.user,
                            ro_status="0")
                        ordID.save()
                        pass
                    
                    ### Create Detail
                    ordDetail = RequestOrderDetail(request_order_id=ordID,product_id=r["partName"],request_qty=r["qty"],balance_qty=r["qty"],request_by_id=request.user,request_status="0")
                    ordDetail.save()
                    
                    ### Update Qty/Item Request Order
                    orderDetail = RequestOrderDetail.objects.filter(request_order_id=ordID)
                    qty = 0
                    item = 0
                    for r in orderDetail:
                        qty +=r.request_qty
                        item += 1
                    
                    ordID.edi_file_id=obj 
                    ordID.ro_item = item
                    ordID.ro_qty = qty
                    ordID.save()
                        
                obj.is_generated = True
                obj.save()
                messages.success(
                    request, f'อัพโหลดเอกสาร {obj.edi_filename} เลขที่ {documentNo} เรียบร้อยแล้ว')
                return redirect('/admin/upload_edi/requestorder/')
            
            except Exception as e:
                # messages.error(request, f'เกิดข้อผิดพลาดในการอัพโหลดเอกสาร')
                messages.error(request, str(e))
                obj.delete()
        else:
            messages.error(request, "กรุณาตรวจสอบข้อมูลส่วนตัวของท่านด้วย")

    def uploaded_at(self, obj):
        return obj.upload_date.strftime("%d-%m-%Y")

    def created_on(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")

    def updated_on(self, obj):
        # return obj.updated_on.strftime("%d %b %Y %H:%M:%S")
        return obj.updated_at.strftime("%d-%m-%Y %H:%M:%S")

    # ordering = ("code","name",)
    list_per_page = 25
    pass


@admin.action(description="Mark selected as Purchase Request")
def make_purchase_request(modeladmin, request, queryset):
    data = queryset
    for obj in data:
        if int(obj.ro_status) < 2:
            # print(obj[0].edi_file_id)
            dte = f'PR{obj.ro_date.strftime("%Y%m%d")[3:]}'
            rnd = PurchaseRequest.objects.filter(purchase_no__gte=dte).count() + 1
            ids = f"{dte}{rnd:05d}"
            data = PurchaseRequest(
                edi_file_id=obj.edi_file_id,
                section_id=request.user.section_id,
                book_id=obj.book_id,
                supplier_id=obj.supplier_id,
                purchase_no=ids,
                purchase_date=obj.ro_date,
                revise_level=obj.edi_file_id.upload_seq,
                item=obj.ro_item,
                qty=obj.ro_qty,
                created_by_id=request.user,
                purchase_status="0",
            )
            # data.save()
            print(data)
            print(obj.id)
            ordDetail = RequestOrderDetail.objects.filter(request_order_id__eq=obj)
            for i in ordDetail:
                print(i.id)
        #     # 
        #     # seq = 1
        #     # for r in obj:
        #     #     pDetail = PurchaseRequestDetail(purchase_request_id=data,request_order_id=r,product_id=r.product_id,seq=seq,qty=r.ro_qty,created_by_id=request.user)
        #     #     pDetail.save()
        #     #     seq += 1
                
        #     # ### Update status
        #     # queryset.update(ro_status="2")


@admin.action(description="Reset To Draff")
def make_draff_request_order(modeladmin, request, queryset):
    queryset.update(ro_status="0")

class ProductRequestOrderInline(admin.TabularInline):
    model = RequestOrderDetail
    readonly_fields = (
        'product_id',
        'request_qty',
        'balance_qty',
        'request_status',
        'updated_at',
    )
    
    fields = [
        'product_id',
        'request_qty',
        'balance_qty',
        'request_status',
        'updated_at',
        'is_selected'
    ]
    
    # def updated_on(self, obj):
    #     # return obj.updated_on.strftime("%d %b %Y %H:%M:%S")
    #     return obj.updated_at.strftime("%d-%m-%Y %H:%M:%S")
    max_num = 0
    extra = 0
    can_delete = True
    can_add = False
    show_change_link = True
    
    def has_change_permission(self, request, obj):
        return True
    
    def has_add_permission(self, request, obj):
        return False
    
class RequestOrderAdmin(admin.ModelAdmin):
    inlines = [ProductRequestOrderInline]
    actions = [make_draff_request_order, make_purchase_request]

    list_filter = ['edi_file_id', 'supplier_id','product_group_id','book_id','ro_status']

    list_select_related = ['edi_file_id']
    
    search_fields = ['ro_no', 'supplier_id']
    
    list_display = [
        'ro_no',
        'get_revise_status',
        'book_id',
        'req_date',
        'product_group_id',
        'ro_item',
        'qty',
        'supplier_id',
        'status',
        'updated_on',
    ]

    fields = [
        'ro_no',
        'book_id',
        'ro_date',
        'product_group_id',
        'ro_item',
        'ro_qty',
        'supplier_id',
        'ro_status',
    ]

    def status(self, obj):
        data = EDI_REQUEST_STATUS[int(obj.ro_status)]
        txtClass = "text-danger"
        if int(obj.ro_status) == 0:
            txtClass = "text-primary"

        elif int(obj.ro_status) == 1:
            txtClass = "text-info"

        elif int(obj.ro_status) == 2:
            txtClass = "text-success"

        elif int(obj.ro_status) == 3:
            txtClass = "text-danger"

        elif int(obj.ro_status) == 4:
            txtClass = "text-info"

        return format_html(f"<span class='{txtClass}'>{data[1]}</span>")

    status.short_description = 'Status'

    def req_date(self, obj):
        return obj.ro_date.strftime("%d-%m-%Y")
    req_date.short_description = "Request Date"

    def created_on(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")
    created_on.short_description = 'Created At'

    def updated_on(self, obj):
        # return obj.updated_on.strftime("%d %b %Y %H:%M:%S")
        return obj.updated_at.strftime("%d-%m-%Y %H:%M:%S")

    def get_revise_status(self, obj):
        return obj.edi_file_id.upload_seq

    get_revise_status.short_description = 'Revise'

    def qty(self, obj):
        return f'{obj.ro_qty:,}'

    def balance(self, obj):
        return f'{obj.balance_qty:,}'

    def get_queryset(self, request):
        print(request)
        qs = super().get_queryset(request)
        return qs

    pass

class ProductPurchaseRequestInline(admin.TabularInline):
    model = PurchaseRequestDetail
    readonly_fields = ('seq','product_id','qty','is_confirm')
    fields = [
        'seq',
        'product_id',
        'qty',
        'is_confirm'
    ]
    extra = 1
    can_delete = False
    can_add = False
    show_change_link = True
    sortable_by = 'seq'
    
    def has_add_permission(self, request, obj):
        return False


class PurchaseRequestAdmin(admin.ModelAdmin):
    inlines = [ProductPurchaseRequestInline]
    list_filter = ['section_id','book_id','supplier_id','purchase_date',]
    list_display = [
        'purchase_no',
        'req_date',
        'book_id',
        'supplier_id',
        'revise_level',
        'item',
        'qty',
        'description',
        'purchase_status',
        'created_on',
        'updated_on',
    ]
    
    date_hierarchy = "purchase_date"
    
    # edi_file_id
    # section_id
    # book_id
    # supplier_id
    # product_group_id
    # purchase_no
    # purchase_date
    # revise_level
    # item0
    # qty
    # description
    fields = [("purchase_no", "revise_level"),"purchase_date", ("item","qty"),"description"]
    # fieldsets = [
    #     (
    #         None,
    #         {
    #             "classes": ["wide", "extrapretty"],
    #             "fields": [("purchase_no", "revise_level",),"purchase_date", "product_group_id"],
    #         },
    #     ),
    #     (
    #         "Advanced options",
    #         {
    #             "classes": ["wide"],
    #             "fields": ["item","qty", "description"],
    #         },
    #     ),
    # ]
    
    def req_date(self, obj):
        return obj.purchase_date.strftime("%d-%m-%Y")
    req_date.short_description = "Date"

    def created_on(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")
    created_on.short_description = 'Created At'

    def updated_on(self, obj):
        # return obj.updated_on.strftime("%d %b %Y %H:%M:%S")
        return obj.updated_at.strftime("%d-%m-%Y %H:%M:%S")
    updated_on.short_description = 'LastUpdate'
    pass

class PurchaseOrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(UploadEDI, UploadEDIAdmin)
admin.site.register(RequestOrder, RequestOrderAdmin)
admin.site.register(PurchaseRequest, PurchaseRequestAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
