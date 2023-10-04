from io import BytesIO
from typing import Any
from django.contrib import admin, messages
from admin_confirm import AdminConfirmMixin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.utils.html import format_html
import nanoid
import pandas as pd
from formula_vcst.models import BOOK, COOR, DEPT, PROD, SECT, UM, NoteCut, OrderH, OrderI

from supplier.models import Book, OrderType, Product, ProductGroup
from .models import EDI_REQUEST_ORDER_STATUS, PURCHASE_ORDER_STATUS, PurchaseOrder, PurchaseOrderDetail, PurchaseRequest, PurchaseRequestDetail, RequestOrder, RequestOrderDetail, UploadEDI
# from .models import UploadEDI, PurchaseRequest, PurchaseOrder, RequestOrder

# Register your models here.


@admin.action(description="Mark selected as Purchase Request", permissions=["change"])
def make_request_request(modeladmin, request, queryset):
    queryset.update(status="p")


class UploadEDIAdmin(admin.ModelAdmin):
    # fields = ('section_id', 'book_id', 'supplier_id', 'product_group_id','edi_file','upload_date','upload_seq','description',)
    confirm_change = True
    confirmation_fields = ['edi_filename', 'is_generated']

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
                    addData.append({"partName": partID, "group_id": partID.prod_group_id,
                                   "qty": r[5], "remark": str(r[1]).strip()})

            # show Message
            try:
                super().save_model(request, obj, form, change)
                for r in addData:
                    # Filter Request Order Header
                    ordID = None
                    try:
                        ordID = RequestOrder.objects.get(supplier_id=obj.supplier_id, section_id=request.user.section_id,
                                                         product_group_id=r["group_id"], book_id=obj.book_id, ro_date=obj.upload_date)
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

                    # Create Detail
                    ordDetail = RequestOrderDetail(request_order_id=ordID, product_id=r["partName"], request_qty=r[
                                                   "qty"], balance_qty=r["qty"], request_by_id=request.user, request_status="0", remark=r["remark"])
                    ordDetail.save()

                    # Update Qty/Item Request Order
                    orderDetail = RequestOrderDetail.objects.filter(
                        request_order_id=ordID)
                    qty = 0
                    item = 0
                    seq = 1
                    for r in orderDetail:
                        qty += r.request_qty
                        item += 1
                        # Update Seq Order Seq
                        r.seq = seq
                        r.save()
                        seq += 1

                    ordID.edi_file_id = obj
                    ordID.ro_item = item
                    ordID.ro_qty = qty
                    ordID.save()

                obj.is_generated = True
                obj.save()
                messages.success(
                    request, f'อัพโหลดเอกสาร {obj.edi_filename} เลขที่ {documentNo} เรียบร้อยแล้ว')

                # SendNotifiedMessage

                # return redirect('/admin/upload_edi/requestorder/')

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


@admin.action(description="Mark selected as Purchase Request", permissions=["change"])
def make_purchase_request(modeladmin, request, queryset):
    try:
        data = queryset
        for obj in data:
            if int(obj.ro_status) < 2:
            # if int(obj.ro_status) < 4:
                # print(obj[0].edi_file_id)
                dte = f'PR{obj.ro_date.strftime("%Y%m%d")[3:]}'
                rnd = PurchaseRequest.objects.filter(
                    purchase_no__gte=dte).count() + 1
                ids = f"{dte}{rnd:05d}"
                pr = PurchaseRequest(
                    request_order_id=obj,
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
                # print(ids)
                pr.save()
                
                # #### Create Formula OrderH
                dept = DEPT.objects.filter(FCCODE=request.user.section_id.code).values()
                sect = SECT.objects.filter(FCCODE=request.user.department_id.code).values()
                ordBook = BOOK.objects.filter(FCREFTYPE="PR", FCCODE="0002").values()
                supplier = COOR.objects.filter(FCCODE=obj.supplier_id.code).values()
                fccode = obj.ro_date.strftime("%Y%m%d")[3:6]
                ordRnd = OrderH.objects.filter(FCCODE__gte=fccode).count() + 1
                fccodeNo = f"{fccode}{ordRnd:04d}"
                prNo = f"TEST{str(ordBook[0]['FCPREFIX']).strip()}{fccodeNo}"
                try:
                    ordH = OrderH(
                        FCSKID=nanoid.generate(size=8),
                        FCREFTYPE="PR",
                        FCDEPT=dept[0]['FCSKID'],
                        FCSECT=sect[0]['FCSKID'],
                        FCBOOK=ordBook[0]['FCSKID'],
                        FCCREATEBY=request.user.id,
                        FCAPPROVEB=request.user.id,
                        FCCODE=fccodeNo,
                        FCREFNO=prNo,
                        FCCOOR=supplier[0]['FCSKID'],
                        FDDATE=obj.ro_date,
                        FDDUEDATE=obj.ro_date,
                        FNAMT=obj.ro_qty,
                    )
                    ordH.save()
                    pr.ref_formula_id=ordH.FCSKID
                    # print(ordH.FCSKID)
                    # Get Order Details
                    ordDetail = RequestOrderDetail.objects.filter(
                        request_order_id=obj).all()
                    seq = 1
                    qty = 0
                    for i in ordDetail:
                        pDetail = PurchaseRequestDetail(
                            purchase_request_id=pr,
                            request_order_id=i,
                            product_group_id=i.product_id.prod_group_id,
                            product_id=i.product_id,
                            seq=seq,
                            qty=i.request_qty,
                            remark=i.remark,
                            is_confirm=False,
                            is_sync=False,
                            created_by_id=request.user,
                        )
                        # Update Status Order Details
                        i.request_status = "2"
                        i.save()
                        
                        ### Create OrderI Formula
                        try:
                            ordProd = PROD.objects.filter(FCCODE=i.product_id.code,FCTYPE=i.product_id.prod_type_id.code).values()
                            unitObj = UM.objects.filter(FCCODE=i.product_id.unit_id.code).values()
                            ordI = OrderI(
                                FCSKID=nanoid.generate(size=8),
                                FCCOOR=supplier[0]['FCSKID'],
                                FCDEPT=dept[0]['FCSKID'],
                                FCORDERH=ordH.FCSKID,
                                FCPROD=ordProd[0]["FCSKID"],
                                FCPRODTYPE=ordProd[0]["FCTYPE"],
                                FCREFTYPE="PR",
                                FCSECT=sect[0]['FCSKID'],
                                FCSEQ=f"{seq:03d}",
                                FCSTUM=unitObj[0]["FCSKID"],
                                FCUM=unitObj[0]["FCSKID"],
                                FCUMSTD=unitObj[0]["FCSKID"],
                                FDDATE=obj.ro_date,
                                FNQTY=i.request_qty,
                                FMREMARK=i.remark,
                                FNBACKQTY=i.request_qty,
                                FNPRICE=ordProd[0]['FNPRICE'],
                                FNPRICEKE=ordProd[0]['FNPRICE'],
                                FCSHOWCOMP="",
                            )
                            ordI.save()
                            
                            pDetail.ref_formula_id=ordI.FCSKID
                            pDetail.save()
                        except Exception as e:
                            messages.error(request, str(e))
                            ordH.delete()
                            return

                        # Summary Seq/Qty
                        seq += 1
                        qty += i.request_qty
                    
                except Exception as e:
                    messages.error(request, str(e))
                    ordH.delete()
                    return
                ### End Formula

            # Update PR Qty
            pr.item = seq-1
            pr.qty = qty
            pr.save()

            # Update Order Status
            queryset.update(ro_status="2")
            messages.success(
                request, f'เพิ่มข้อมูล PR เอกสารเลขที่ {pr} เรียบร้อยแล้ว')

            # SendNotifiedMessage

    except:
        # Update Order Status When Error
        queryset.update(ro_status="3")
        messages.error(request, "เกิดข้อผิดพลาดระหว่างการบันทึกข้อมูล!")
        pass


@admin.action(description="Reset To Draff", permissions=["change"])
def make_draff_request_order(modeladmin, request, queryset):
    queryset.update(ro_status="0")


class ProductRequestOrderInline(admin.TabularInline):
    model = RequestOrderDetail
    readonly_fields = (
        'seq',
        'product_id',
        'request_qty',
        'balance_qty',
        'request_status',
        'updated_at',
    )

    fields = [
        'seq',
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        print(request.build_absolute_uri)
        # for i in qs:
        #     print(f"{i.request_order_id} ID: {i.id} STATUS: {i.request_status}")

        return qs.filter(request_status__lte="1")


class RequestOrderAdmin(AdminConfirmMixin, admin.ModelAdmin):
    change_form_template = 'admin/save_request_order_change_form.html'
    confirm_change = True
    confirmation_fields = ['ro_status']
    inlines = [ProductRequestOrderInline]
    actions = [make_draff_request_order, make_purchase_request]

    list_filter = ['edi_file_id', 'supplier_id',
                   'product_group_id', 'book_id', 'ro_status']
    list_select_related = ['edi_file_id']
    search_fields = ['ro_no', 'supplier_id']
    list_per_page = 25

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

    def get_readonly_fields(self, request, obj):
        lst = ('product_group_id', 'supplier_id',
               'ro_no', 'ro_item', 'ro_qty', 'ro_status',)
        if int(obj.ro_status) == 2:
            lst += ('book_id', 'ro_date',)

        return lst

    def status(self, obj):
        data = EDI_REQUEST_ORDER_STATUS[int(obj.ro_status)]
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
        qs = super().get_queryset(request)
        return qs

    # Set Overrides Message
    def message_user(self, request, message, level=messages.INFO, extra_tags='', fail_silently=False):
        pass

    # Create Overrides Save Methods
    def save_model(self, request, obj, form, change):
        return super().save_model(request, obj, form, change)

    # Overrides Update Methods
    def response_change(self, request, obj):
        if "_send_to_pr" in request.POST:
            if int(obj.ro_status) < 2:
                dte = f'PR{obj.ro_date.strftime("%Y%m%d")[3:]}'
                rnd = PurchaseRequest.objects.filter(
                    purchase_no__gte=dte).count() + 1
                ids = f"{dte}{rnd:05d}"
                pr = PurchaseRequest(
                    request_order_id=obj,
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
                pr.save()

                # Get Order Details
                ordDetail = RequestOrderDetail.objects.filter(
                    request_order_id=obj).all()
                seq = 1
                qty = 0
                balance_qty = 0
                for i in ordDetail:
                    if i.is_selected and i.request_status == "0":
                        pDetail = PurchaseRequestDetail(
                            purchase_request_id=pr,
                            request_order_id=i,
                            product_group_id=i.product_id.prod_group_id,
                            product_id=i.product_id,
                            seq=seq,
                            qty=i.request_qty,
                            remark=i.remark,
                            is_confirm=False,
                            is_sync=False,
                            created_by_id=request.user,
                        )
                        pDetail.save()
                        # Update Status Order Details
                        i.request_status = "2"
                        i.save()

                        # Summary Seq/Qty
                        seq += 1
                        qty += i.request_qty
                    else:
                        balance_qty += i.request_qty

                # Update PR Qty
                pr.item = seq-1
                pr.qty = qty
                pr.save()

                # Check Order Status
                obj_status = "2"  # กรณีที่ครบ
                if obj.ro_item != pr.item:
                    obj_status = "1"  # กรณีที่ไม่ครบ
                # Update Order Status
                obj.ro_status = obj_status

                obj.ro_item -= pr.item
                obj.qty = balance_qty
                obj.save()
                messages.success(
                    request, f'เพิ่มข้อมูล PR เอกสารเลขที่ {pr} เรียบร้อยแล้ว')

                # SendNotifiedMessage

        return super().response_change(request, object)

    pass


class ProductPurchaseRequestInline(admin.TabularInline):
    model = PurchaseRequestDetail
    readonly_fields = ('seq', 'product_group_id',
                       'product_id', 'qty', 'is_confirm')
    fields = [
        'seq',
        'product_group_id',
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


@admin.action(description="Create Purchase Order", permissions=["change"])
def make_purchase_order(modeladmin, request, queryset):
    data = queryset
    for obj in data:
        pref = f"PO{obj.purchase_date.strftime('%Y%m%d')[3:]}"
        rnd = PurchaseOrder.objects.filter(order_no__gte=pref).count() + 1
        ids = f"{pref}{rnd:05d}"
        poHeader = PurchaseOrder(purchase_id=obj, order_no=ids, order_date=obj.purchase_date, item=obj.item,
                                 qty=obj.qty, order_status="0", description=obj.description, created_by_id=request.user)
        poHeader.save()
        
        #### Create Order Header
        dept = DEPT.objects.filter(FCCODE=request.user.section_id.code).values()
        sect = SECT.objects.filter(FCCODE=request.user.department_id.code).values()
        ordBook = BOOK.objects.filter(FCREFTYPE="PO", FCCODE="002").values()
        supplier = COOR.objects.filter(FCCODE=obj.supplier_id.code).values()
        fccode = obj.purchase_date.strftime("%Y%m%d")[3:6]
        ordRnd = OrderH.objects.filter(FCCODE__gte=fccode).count() + 1
        fccodeNo = f"{fccode}{ordRnd:04d}"
        prNo = f"TEST{str(ordBook[0]['FCPREFIX']).strip()}{fccodeNo}"
        
        try:
            ordH = OrderH(
                FCSKID=nanoid.generate(size=8),
                FCREFTYPE="PO",
                FCDEPT=dept[0]['FCSKID'],
                FCSECT=sect[0]['FCSKID'],
                FCBOOK=ordBook[0]['FCSKID'],
                FCCREATEBY=request.user.id,
                FCAPPROVEB=request.user.id,
                FCCODE=fccodeNo,
                FCREFNO=prNo,
                FCCOOR=supplier[0]['FCSKID'],
                FDDATE=obj.purchase_date,
                FDDUEDATE=obj.purchase_date,
                FNAMT=obj.qty,
            )
            ordH.save()
            # print(ordH.FCSKID)
            prDetail = PurchaseRequestDetail.objects.filter(purchase_request_id=obj).all()
            for pr in prDetail:
                poDetail = PurchaseOrderDetail(
                    purchase_order_id=poHeader,
                    product_group_id=pr.product_group_id,
                    product_id=pr.product_id,
                    seq=pr.seq,
                    qty=pr.qty,
                    remark=pr.remark,
                    is_active=True,
                    created_by_id=request.user
                )
                
                
                ### Create OrderI Formula
                try:
                    ordProd = PROD.objects.filter(FCCODE=pr.product_id.code,FCTYPE=pr.product_id.prod_type_id.code).values()
                    unitObj = UM.objects.filter(FCCODE=pr.product_id.unit_id.code).values()
                    ordI = OrderI(
                        FCSKID=nanoid.generate(size=8),
                        FCCOOR=supplier[0]['FCSKID'],
                        FCDEPT=dept[0]['FCSKID'],
                        FCORDERH=ordH.FCSKID,
                        FCPROD=ordProd[0]["FCSKID"],
                        FCPRODTYPE=ordProd[0]["FCTYPE"],
                        FCREFTYPE="PO",
                        FCSECT=sect[0]['FCSKID'],
                        FCSEQ=f"{pr.seq:03d}",
                        FCSTUM=unitObj[0]["FCSKID"],
                        FCUM=unitObj[0]["FCSKID"],
                        FCUMSTD=unitObj[0]["FCSKID"],
                        FDDATE=obj.purchase_date,
                        FNQTY=pr.qty,
                        FMREMARK=pr.remark,
                        FNBACKQTY=pr.qty,
                        FNPRICE=ordProd[0]['FNPRICE'],
                        FNPRICEKE=ordProd[0]['FNPRICE'],
                        FCSHOWCOMP="",
                    )
                    
                    ordI.save()
                    poDetail.ref_formula_id=ordI.FCSKID
                    poDetail.save()
                    
                    ### Create Notecut
                    orderPRID = obj.ref_formula_id
                    orderPRDetailID = pr.ref_formula_id
                    
                    
                    orderPOID = ordH.FCSKID
                    orderPODetailID = ordI.FCSKID
                    
                    print(f"H: {orderPRID} HD: {orderPRDetailID} ==> P: {orderPOID} PD: {orderPODetailID}")
                    noteCut = NoteCut(
                        FCAPPNAME="",
                        FCSKID=nanoid.generate(size=8),
                        FCCHILDH=orderPRID,
                        FCCHILDI=orderPRDetailID,
                        FCMASTERH=orderPOID,
                        FCMASTERI=orderPODetailID,
                        FNQTY=pr.qty,
                        FNUMQTY=pr.qty,
                        FCCORRECTB="",
                        FCCREATEBY="",
                        FCCREATETY="",
                        FCCUACC="",
                        FCDATAIMP="",
                        FCORGCODE="",
                        FCSELTAG="",
                        FCSRCUPD="",
                        FCU1ACC="",
                        FCUDATE="",
                        FCUTIME="",
                    )
                    noteCut.save()
                    
                except Exception as e:
                    messages.error(request, str(e))
                    ordH.delete()
                    poHeader.delete()
                    return

                # Update Purchase Request
                pr.is_confirm = True
                pr.save()
                
            poHeader.ref_formula_id=ordH.FCSKID
            poHeader.save()
            queryset.update(purchase_status="2")
            messages.success(request, f'เพิ่มข้อมูล PO เอกสารเลขที่ {poHeader} เรียบร้อยแล้ว')
            
        except Exception as e:
            messages.error(request, str(e))
            ordH.delete()
            pass


class PurchaseRequestAdmin(AdminConfirmMixin, admin.ModelAdmin):
    confirm_change = True
    confirmation_fields = ['field1', 'field2']
    actions = [make_purchase_order]

    inlines = [ProductPurchaseRequestInline]
    list_filter = ['section_id', 'book_id', 'supplier_id', 'purchase_date',]
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
    list_select_related = ['request_order_id']

    fields = [("purchase_no", "revise_level"),"purchase_date", ("item", "qty"), "description"]
    readonly_fields = ["purchase_no", "revise_level","purchase_date","item", "qty", "description"]
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


class PurchaseOrderDetailInline(admin.TabularInline):
    model = PurchaseOrderDetail
    readonly_fields = [
        "seq",
        "product_group_id",
        "product_id",
        "qty",
        "is_active",
    ]

    fields = [
        "seq",
        "product_group_id",
        "product_id",
        "qty",
        "is_active",
    ]

    extra = 1
    can_delete = False
    can_add = False
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False


@admin.action(description="Recheck Order")
def recheck_order(modeladmin, request, queryset):
    queryset.update(order_status="0")


class PurchaseOrderAdmin(admin.ModelAdmin):
    inlines = [PurchaseOrderDetailInline]
    list_display = [
        "order_no",
        "req_date",
        "item",
        "qty",
        "status",
        "is_sync",
        "updated_on",
    ]

    fields = [
        "order_no",
        "order_date",
        "item",
        "qty",
        "order_status",
        'description',
    ]

    list_filter = [
        "purchase_id",
        "order_date",
        "order_status",
    ]

    readonly_fields = [
        "order_no",
        "item",
        "qty",
        "order_status",
    ]
    search_fields = ["order_no"]
    date_hierarchy = "order_date"
    actions = [recheck_order]
    list_per_page = 25
    
    def req_date(self, obj):
        return obj.order_date.strftime("%d-%m-%Y")
    
    req_date.short_description = "Date"
    
    def created_on(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")
    created_on.short_description = 'Created At'

    def updated_on(self, obj):
        # return obj.updated_on.strftime("%d %b %Y %H:%M:%S")
        return obj.updated_at.strftime("%d-%m-%Y %H:%M:%S")
    updated_on.short_description = 'LastUpdate'
    
    def status(self, obj):
        data = PURCHASE_ORDER_STATUS[int(obj.order_status)]
        txtClass = "text-danger"
        if int(obj.order_status) == 0:
            txtClass = "text-primary"

        elif int(obj.order_status) == 1:
            txtClass = "text-info"

        elif int(obj.order_status) == 2:
            txtClass = "text-success"

        elif int(obj.order_status) == 3:
            txtClass = "text-danger"

        elif int(obj.order_status) == 4:
            txtClass = "text-info"

        return format_html(f"<span class='{txtClass}'>{data[1]}</span>")
    pass


admin.site.register(UploadEDI, UploadEDIAdmin)
admin.site.register(RequestOrder, RequestOrderAdmin)
admin.site.register(PurchaseRequest, PurchaseRequestAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
