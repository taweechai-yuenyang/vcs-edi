from django.contrib import admin, messages
import pandas as pd

from supplier.models import Book, OrderType, ProductGroup
from .models import UploadEDI, RequestOrder
# from .models import UploadEDI, PurchaseRequest, PurchaseOrder, RequestOrder

# Register your models here.


@admin.action(description="Mark selected as Purchase Request")
def make_request_request(modeladmin, request, queryset):
    queryset.update(status="p")


class UploadEDIAdmin(admin.ModelAdmin):
    # fields = ('section_id', 'book_id', 'supplier_id', 'product_group_id','edi_file','upload_date','upload_seq','description',)
    actions = [make_request_request]

    list_filter = ['is_generated','document_no', 'edi_filename', 'upload_seq']
    
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
            
            ### Read Excel
            file_in_memory = request.FILES['edi_file'].read()
            data = pd.read_excel(file_in_memory).to_numpy()
            for r in data:
                modelID = r[1]
                partNo = r[2]
                partName = r[3]
                partDescription = r[4]
                
                print(modelID)
                mdID = ProductGroup.objects.get(code=modelID)
                print(mdID)
            

            # # show Message
            # try:
            #     super().save_model(request, obj, form, change)
            #     messages.success(
            #         request, f'อัพโหลดเอกสาร {obj.edi_filename} เลขที่ {documentNo} เรียบร้อยแล้ว')
            # except:
            #     messages.error(request, f'เกิดข้อผิดพลาดในการอัพโหลดเอกสาร')
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
    queryset.update(status="p")


class RequestOrderAdmin(admin.ModelAdmin):
    actions = [make_purchase_request]
    pass

# class PurchaseRequestAdmin(admin.ModelAdmin):
#     pass

# class PurchaseOrderAdmin(admin.ModelAdmin):
#     pass


admin.site.register(UploadEDI, UploadEDIAdmin)
admin.site.register(RequestOrder, RequestOrderAdmin)
# admin.site.register(PurchaseRequest, PurchaseRequestAdmin)
# admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
