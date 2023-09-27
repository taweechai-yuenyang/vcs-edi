from django import forms
from django.forms import ModelForm
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import Group
from .models import Supplier, OrderType, ProductType, Unit, Product

# # Register your models here.
# class SupplierForm(ModelForm):
#     description = forms.CharField(widget=CKEditorWidget())
#     class Meta:
#         model = Supplier
#         fields = '__all__'

class SupplierAdmin(admin.ModelAdmin):
    # change_list_template = "admin/change_list.html"
    # form = SupplierForm
    
    list_display = (
        # 'skid',
        'code',
        'name',
        # 'user_id',
        'description',
        'is_active',
        'created_at',
        'updated_at',
    )
    
    search_fields = (
        'skid',
        'code',
        'name',
    )
    
    list_filter = (
        'is_active',
        'user_id',
    )
    
    # list_editable = (
    #     'code',
    #     'name',
    #     'is_active',
    # )
    
    fieldsets = (
        ("", {
            "fields": (
                ("user_id",),
                ("skid",),
                ("code",),
                ("name",),
                ("description",),
                "is_active",
                ),
        }),
    )
    
    # fieldsets = (
    #     ("ข้อมูลผู้ใช้งาน", {
    #         "fields": ("user_id",)
    #     }),
        
    #     ("รายละเอียดเพิ่มเติม", {
    #         "fields": (
    #             ("skid",),
    #             ("code",),
    #             ("name",),
    #             ("description",),
    #             "is_active",
    #             ),
    #     }),
    # )
    
    # ordering = ("code","name",)
    list_per_page = 25
    
    def created_at(self, obj):
        return obj.created_on.strftime("%d-%m-%Y %H:%M:%S")
    
    def updated_at(self, obj):
        # return obj.updated_on.strftime("%d %b %Y %H:%M:%S")
        return obj.updated_on.strftime("%d-%m-%Y %H:%M:%S")
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        isStaff = False
        query_set = Group.objects.filter(user = request.user)
        for g in query_set:
            if g.name.find("VCS") >= 0:
                isStaff = True
                break

        if isStaff:
            return qs

        return qs.filter(user_id=request.user)
    
    pass

class ProductTypeAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'name',
        'description',
        'is_active',
        'created_at',
        'updated_at',
    )
    
    search_fields = (
        'code',
        'name',
    )
    
    list_filter = ('is_active',)
    
    # ordering = ("code","name",)
    list_per_page = 25
    
    def created_at(self, obj):
        return obj.created_on.strftime("%d-%m-%Y %H:%M:%S")
    
    def updated_at(self, obj):
        # return obj.updated_on.strftime("%d %b %Y %H:%M:%S")
        return obj.updated_on.strftime("%d-%m-%Y %H:%M:%S")
    pass

class UnitAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'name',
        'description',
        'is_active',
        'created_at',
        'updated_at',
    )
    
    search_fields = (
        'code',
        'name',
    )
    
    list_filter = ('is_active',)
    
    # ordering = ("code","name",)
    list_per_page = 25
    
    def created_at(self, obj):
        return obj.created_on.strftime("%d-%m-%Y %H:%M:%S")
    
    def updated_at(self, obj):
        # return obj.updated_on.strftime("%d %b %Y %H:%M:%S")
        return obj.updated_on.strftime("%d-%m-%Y %H:%M:%S")
    pass

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'prod_type_id',
        'code',
        'name',
        'description',
        'is_active',
        'created_at',
        'updated_at',
    )
    
    search_fields = (
        'code',
        'name',
    )
    
    list_filter = ('prod_type_id','is_active',)
    
    # ordering = ("code","name",)
    list_per_page = 25
    
    def created_at(self, obj):
        return obj.created_on.strftime("%d-%m-%Y %H:%M:%S")
    
    def updated_at(self, obj):
        # return obj.updated_on.strftime("%d %b %Y %H:%M:%S")
        return obj.updated_on.strftime("%d-%m-%Y %H:%M:%S")
    pass

class OrderTypeAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'name',
        'description',
        'is_active',
        'created_at',
        'updated_at',
    )
    
    search_fields = (
        'code',
        'name',
    )
    
    list_filter = ('is_active',)
    
    # ordering = ("code","name",)
    list_per_page = 25
    
    def created_at(self, obj):
        return obj.created_on.strftime("%d-%m-%Y %H:%M:%S")
    
    def updated_at(self, obj):
        # return obj.updated_on.strftime("%d %b %Y %H:%M:%S")
        return obj.updated_on.strftime("%d-%m-%Y %H:%M:%S")
    pass

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderType, OrderTypeAdmin)