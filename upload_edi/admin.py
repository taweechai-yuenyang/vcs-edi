from io import BytesIO
from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.utils.html import format_html
import pandas as pd

from supplier.models import Book, OrderType, Product, ProductGroup
from .models import EDI_REQUEST_STATUS, PurchaseOrder, PurchaseRequest, PurchaseRequestDetail, UploadEDI, RequestOrder
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
                    'supplier_id', 'product_group_id', 'edi_file', 'description',
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
                    addData.append({"partName": r[3], "qty": r[5]})

            # show Message
            try:
                super().save_model(request, obj, form, change)
                for r in addData:
                    partID = Product.objects.get(code=r['partName'])
                    dataObj = RequestOrder(edi_file_id=obj,supplier_id=obj.supplier_id,section_id=obj.section_id,book_id=obj.book_id,product_group_id=obj.product_group_id, product_id=partID, request_date=obj.upload_date, request_qty=r['qty'], balance_qty=r['qty'], request_by_id=request.user, request_status="0")
                    dataObj.save()

                obj.is_generated = True
                obj.save()

                messages.success(
                    request, f'อัพโหลดเอกสาร {obj.edi_filename} เลขที่ {documentNo} เรียบร้อยแล้ว')

                return redirect('/admin/upload_edi/requestorder/')

            except Exception as e:
                # messages.error(request, f'เกิดข้อผิดพลาดในการอัพโหลดเอกสาร')
                messages.error(request, str(e))
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
    obj = queryset
    if int(obj[0].request_status) < 2:
        # print(obj[0].edi_file_id)
        dte = f'PR{obj[0].request_date.strftime("%Y%m%d")[3:]}'
        rnd = PurchaseRequest.objects.filter(purchase_no__gt=dte).count() + 1
        ids = f"{dte}{rnd:05d}"
        qty = 0
        for r in obj:
            qty += r.request_qty
        
        data = PurchaseRequest(
            edi_file_id=obj[0].edi_file_id,
            section_id=obj[0].section_id,
            book_id=obj[0].book_id,
            supplier_id=obj[0].supplier_id,
            product_group_id=obj[0].product_group_id,
            purchase_no=ids,
            purchase_date=obj[0].request_date,
            revise_level=obj[0].edi_file_id.upload_seq,
            item=len(obj),
            qty=qty,
            created_by_id=request.user,
            purchase_status="0",
        )
        data.save()
        seq = 1
        for r in obj:
            pDetail = PurchaseRequestDetail(purchase_request_id=data,request_order_id=r,product_id=r.product_id,seq=seq,qty=r.request_qty,created_by_id=request.user)
            pDetail.save()
            seq += 1
            
        ### Update status
        queryset.update(request_status="2")


@admin.action(description="Reset To Draff")
def make_draff_request_order(modeladmin, request, queryset):
    queryset.update(request_status="0")
    
class RequestOrderAdmin(admin.ModelAdmin):
    actions = [make_draff_request_order, make_purchase_request]

    list_filter = ['edi_file_id', 'product_group_id','supplier_id','book_id','request_status']

    list_display = [
        'edi_file_id',
        'book_id',
        'req_date',
        'get_model_data',
        'product_id',
        'qty',
        'supplier_id',
        'status',
        'updated_on',
    ]

    fields = [
        'product_group_id',
        'product_id',
        'request_qty',
        'request_date',
        'request_status'
    ]

    def status(self, obj):
        data = EDI_REQUEST_STATUS[int(obj.request_status)]
        txtClass = "text-danger"
        if int(obj.request_status) == 0:
            txtClass = "text-primary"

        elif int(obj.request_status) == 1:
            txtClass = "text-info"

        elif int(obj.request_status) == 2:
            txtClass = "text-success"

        elif int(obj.request_status) == 3:
            txtClass = "text-danger"

        elif int(obj.request_status) == 4:
            txtClass = "text-info"

        return format_html(f"<span class='{txtClass}'>{data[1]}</span>")

    status.short_description = 'Status'

    def req_date(self, obj):
        return obj.request_date.strftime("%d-%m-%Y")
    req_date.short_description = "Request Date"

    def created_on(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")
    created_on.short_description = 'Created At'

    def updated_on(self, obj):
        # return obj.updated_on.strftime("%d %b %Y %H:%M:%S")
        return obj.updated_at.strftime("%d-%m-%Y %H:%M:%S")

    def get_model_data(self, obj):
        return obj.edi_file_id.product_group_id

    get_model_data.short_description = 'Model'

    def qty(self, obj):
        return f'{obj.request_qty:,}'

    def balance(self, obj):
        return f'{obj.balance_qty:,}'

    def get_queryset(self, request):
        print(request)
        qs = super().get_queryset(request)
        return qs

    pass

class ProductPurchaseRequestInline(admin.TabularInline):
    model = PurchaseRequestDetail
    readonly_fields = ('seq','product_id','qty')
    fields = [
        'seq',
        'product_id',
        'qty',
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
    list_filter = ['section_id','book_id','supplier_id','product_group_id','purchase_date',]
    list_display = [
        'purchase_no',
        'req_date',
        'book_id',
        'supplier_id',
        'product_group_id',
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
    fields = [("purchase_no", "revise_level"),"purchase_date", "product_group_id",("item","qty"),"description"]
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
