import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    user_id = models.ForeignKey(User, blank=True, verbose_name="User ID", on_delete=models.SET_NULL, null=True)
    skid = models.CharField(max_length=8, verbose_name="Formula ID", unique=True, blank=False, null=False)
    code = models.CharField(max_length=150, verbose_name="Code", unique=True, blank=False, null=False)
    name = models.CharField(max_length=150, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description", blank=True, default="-")
    # description = HTMLField()
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        # db_table_comment = "formula_vcst"
        # app_label = "budgetaaa"
        # ordering = ('-updated_on','code','name')
        db_table = "tbtSupplier"
        verbose_name = "ข้อมูล Supplier"
        verbose_name_plural = "Supplier"