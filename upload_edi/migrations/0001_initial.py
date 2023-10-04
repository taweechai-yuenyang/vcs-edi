# Generated by Django 4.2.5 on 2023-10-04 06:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('order_no', models.CharField(max_length=50, verbose_name='Order No')),
                ('order_date', models.DateField(verbose_name='Order Date')),
                ('item', models.IntegerField(default='0', verbose_name='Item')),
                ('qty', models.FloatField(default='0.0', verbose_name='Qty.')),
                ('order_status', models.CharField(default='0', max_length=1, verbose_name='Order Status')),
                ('description', models.TextField(blank=True, default='-', null=True, verbose_name='Description')),
                ('is_sync', models.BooleanField(default=False, verbose_name='Is Sync')),
                ('ref_formula_id', models.CharField(blank=True, max_length=8, null=True, verbose_name='Ref. Formula ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created By ID')),
            ],
            options={
                'verbose_name': 'PO',
                'verbose_name_plural': '4.Purchase Order',
                'db_table': 'ediPO',
            },
        ),
        migrations.CreateModel(
            name='PurchaseRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('purchase_no', models.CharField(max_length=50, verbose_name='Purchase No')),
                ('purchase_date', models.DateField(verbose_name='Purchase Date')),
                ('revise_level', models.CharField(choices=[('0', 'Revise 0'), ('1', 'Revise 1'), ('2', 'Revise 2'), ('3', 'Revise 3'), ('4', 'Revise 4'), ('5', 'Revise 5')], default='0', max_length=1, verbose_name='Revise Level')),
                ('item', models.IntegerField(default='0', verbose_name='Item')),
                ('qty', models.FloatField(default='0.0', verbose_name='Qty.')),
                ('description', models.TextField(blank=True, default='-', null=True, verbose_name='Description')),
                ('purchase_status', models.CharField(blank=True, choices=[('0', 'Draff'), ('1', 'In Process'), ('2', 'Success'), ('3', 'Failure')], default='0', max_length=1, null=True, verbose_name='Purchase Status')),
                ('ref_formula_id', models.CharField(blank=True, max_length=8, null=True, verbose_name='Ref. Formula ID')),
                ('is_sync', models.BooleanField(default=False, verbose_name='Status Sync')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.book', verbose_name='Book ID')),
                ('created_by_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created By ID')),
            ],
            options={
                'verbose_name': 'PR',
                'verbose_name_plural': '3.Purchase Request',
                'db_table': 'ediPR',
                'ordering': ('purchase_status', 'purchase_no', 'purchase_date'),
            },
        ),
        migrations.CreateModel(
            name='RequestOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('ro_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='Request No.')),
                ('ro_date', models.DateField(blank=True, null=True, verbose_name='Request Date')),
                ('ro_item', models.IntegerField(blank=True, default='0', null=True, verbose_name='Item')),
                ('ro_qty', models.FloatField(blank=True, default='0', null=True, verbose_name='Qty.')),
                ('ro_status', models.CharField(choices=[('0', 'Draff'), ('1', 'In Process'), ('2', 'Success'), ('3', 'Failure')], default='0', max_length=1, verbose_name='Request Status')),
                ('ref_formula_id', models.CharField(blank=True, max_length=8, null=True, verbose_name='Ref. Formula ID')),
                ('is_sync', models.BooleanField(default=False, verbose_name='Is Sync')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('book_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='supplier.book', verbose_name='Book ID')),
            ],
            options={
                'verbose_name': 'RO',
                'verbose_name_plural': '2.Request Order',
                'db_table': 'ediRO',
                'ordering': ('ro_status', 'ro_date', 'ro_no'),
            },
        ),
        migrations.CreateModel(
            name='UploadEDI',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('edi_file', models.FileField(upload_to='upload_edi/static/edi/%Y-%m-%d/', verbose_name='FILE EDI')),
                ('edi_filename', models.CharField(blank=True, editable=False, max_length=150, null=True, unique=True, verbose_name='FILE EDI')),
                ('document_no', models.CharField(blank=True, editable=False, max_length=150, null=True, verbose_name='Document No.')),
                ('upload_date', models.DateField(default=django.utils.timezone.now, verbose_name='Upload On')),
                ('upload_seq', models.CharField(choices=[('0', 'Revise 0'), ('1', 'Revise 1'), ('2', 'Revise 2'), ('3', 'Revise 3'), ('4', 'Revise 4'), ('5', 'Revise 5')], default='0', max_length=1, verbose_name='Revise Level')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_generated', models.BooleanField(default=False, verbose_name='Is Generated')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('book_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='supplier.book', verbose_name='Book ID')),
                ('section_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='supplier.section', verbose_name='Section ID')),
                ('supplier_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.supplier', verbose_name='Supplier ID')),
                ('upload_by_id', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Upload By ID')),
            ],
            options={
                'verbose_name': 'FileEDI',
                'verbose_name_plural': '1.Upload File EDI',
                'db_table': 'ediFileUpload',
            },
        ),
        migrations.CreateModel(
            name='RequestOrderDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('seq', models.IntegerField(blank=True, default='0', null=True, verbose_name='Sequence')),
                ('request_qty', models.FloatField(default='0.0', verbose_name='Request Qty.')),
                ('balance_qty', models.FloatField(default='0.0', verbose_name='Balance Qty.')),
                ('request_status', models.CharField(choices=[('0', 'Draff'), ('1', 'In Process'), ('2', 'Success'), ('3', 'Failure')], default='0', max_length=1, verbose_name='Request Status')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='Remark')),
                ('is_selected', models.BooleanField(default=True, verbose_name='Is Selected')),
                ('is_sync', models.BooleanField(default=False, verbose_name='Is Sync')),
                ('ref_formula_id', models.CharField(blank=True, max_length=8, null=True, verbose_name='Ref. Formula ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.product', verbose_name='Product ID')),
                ('request_by_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Request By ID')),
                ('request_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload_edi.requestorder', verbose_name='Request ID')),
            ],
            options={
                'verbose_name': 'RO Detail',
                'verbose_name_plural': 'Request Order Detail',
                'db_table': 'ediRODetail',
                'ordering': ('seq', 'product_id', 'created_at', 'updated_at'),
            },
        ),
        migrations.AddField(
            model_name='requestorder',
            name='edi_file_id',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='upload_edi.uploadedi', verbose_name='EDI File ID'),
        ),
        migrations.AddField(
            model_name='requestorder',
            name='product_group_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='supplier.productgroup', verbose_name='Model ID'),
        ),
        migrations.AddField(
            model_name='requestorder',
            name='ro_by_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Request By ID'),
        ),
        migrations.AddField(
            model_name='requestorder',
            name='section_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='supplier.section', verbose_name='Section ID'),
        ),
        migrations.AddField(
            model_name='requestorder',
            name='supplier_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='supplier.supplier', verbose_name='Supplier ID'),
        ),
        migrations.CreateModel(
            name='PurchaseRequestDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('seq', models.IntegerField(blank=True, default='0', null=True, verbose_name='Sequence')),
                ('qty', models.FloatField(default='0.0', verbose_name='Qty.')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='Remark')),
                ('is_confirm', models.BooleanField(default=False, verbose_name='Confirmed')),
                ('is_sync', models.BooleanField(default=False, verbose_name='Status Sync')),
                ('ref_formula_id', models.CharField(blank=True, max_length=8, null=True, verbose_name='Ref. Formula ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created By ID')),
                ('product_group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.productgroup', verbose_name='Model ID')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.product', verbose_name='Product ID')),
                ('purchase_request_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload_edi.purchaserequest', verbose_name='Purchase Request ID')),
                ('request_order_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='upload_edi.requestorderdetail', verbose_name='Order Detail ID')),
            ],
            options={
                'verbose_name': 'PR Detail',
                'verbose_name_plural': 'Purchase Request Detail',
                'db_table': 'ediPRDetail',
                'ordering': ['purchase_request_id', 'seq'],
            },
        ),
        migrations.AddField(
            model_name='purchaserequest',
            name='request_order_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='upload_edi.requestorder', verbose_name='Request Order ID'),
        ),
        migrations.AddField(
            model_name='purchaserequest',
            name='section_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.section', verbose_name='Section ID'),
        ),
        migrations.AddField(
            model_name='purchaserequest',
            name='supplier_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.supplier', verbose_name='Supplier ID'),
        ),
        migrations.CreateModel(
            name='PurchaseOrderDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('seq', models.IntegerField(blank=True, default='0', null=True, verbose_name='Sequence')),
                ('qty', models.FloatField(default='0.0', verbose_name='Qty.')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='Remark')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is Active')),
                ('is_sync', models.BooleanField(default=False, verbose_name='Is Sync')),
                ('ref_formula_id', models.CharField(blank=True, max_length=8, null=True, verbose_name='Ref. Formula ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created By ID')),
                ('product_group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.productgroup', verbose_name='Model ID')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.product', verbose_name='Product ID')),
                ('purchase_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload_edi.purchaseorder', verbose_name='Purchase Order ID')),
            ],
            options={
                'verbose_name': 'PO Detail',
                'verbose_name_plural': 'Purchase Order Detail',
                'db_table': 'ediPODetail',
            },
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='purchase_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload_edi.purchaserequest', verbose_name='Purchase ID'),
        ),
        migrations.CreateModel(
            name='ApproveRequestOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('request_status', models.CharField(choices=[('0', 'Draff'), ('1', 'In Process'), ('2', 'Success'), ('3', 'Failure')], default='0', max_length=1, verbose_name='Request Status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('request_by_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Request By ID')),
                ('request_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload_edi.requestorder', verbose_name='Request ID')),
            ],
            options={
                'verbose_name': 'Approve RO',
                'verbose_name_plural': 'Approve Request Order',
                'db_table': 'ediROApprove',
            },
        ),
        migrations.CreateModel(
            name='ApprovePurchaseRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('purchase_request_status', models.CharField(choices=[('0', 'Draff'), ('1', 'In Process'), ('2', 'Success'), ('3', 'Failure')], default='0', max_length=1, verbose_name='Purchase Request Status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approve_by_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Approve By ID')),
                ('request_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload_edi.purchaserequest', verbose_name='Purchase Request ID')),
            ],
            options={
                'verbose_name': 'Approve PR',
                'verbose_name_plural': 'Approve Purchase Request',
                'db_table': 'ediPRApprove',
            },
        ),
        migrations.CreateModel(
            name='ApprovePurchaseOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('purchase_request_status', models.CharField(choices=[('0', 'Draff'), ('1', 'Wait for Approve'), ('2', 'Approve'), ('3', 'Cancel'), ('4', 'Reject'), ('5', 'Revise')], default='0', max_length=1, verbose_name='Purchase Order Status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approve_by_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Approve By ID')),
                ('purchase_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload_edi.purchaseorder', verbose_name='Purchase Request ID')),
            ],
            options={
                'verbose_name': 'Approve PO',
                'verbose_name_plural': 'Approve Purchase Order',
                'db_table': 'ediPOApprove',
            },
        ),
    ]
