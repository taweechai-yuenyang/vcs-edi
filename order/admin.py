from django.contrib import admin
from .models import OrderHead,OrderDetail

# Register your models here.
class OrderHeadAdmin(admin.ModelAdmin):
    pass

class OrderDetailAdmin(admin.ModelAdmin):
    pass

admin.site.register(OrderHead,OrderHeadAdmin)
admin.site.register(OrderDetail,OrderDetailAdmin)
