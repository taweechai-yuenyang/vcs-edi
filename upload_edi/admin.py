from django.contrib import admin
from .models import UploadEDI, RequestOrder
# from .models import UploadEDI, PurchaseRequest, PurchaseOrder, RequestOrder

# Register your models here.
class UploadEDIAdmin(admin.ModelAdmin):
    pass

class RequestOrderAdmin(admin.ModelAdmin):
    pass

# class PurchaseRequestAdmin(admin.ModelAdmin):
#     pass

# class PurchaseOrderAdmin(admin.ModelAdmin):
#     pass

admin.site.register(UploadEDI, UploadEDIAdmin)
admin.site.register(RequestOrder, RequestOrderAdmin)
# admin.site.register(PurchaseRequest, PurchaseRequestAdmin)
# admin.site.register(PurchaseOrder, PurchaseOrderAdmin)