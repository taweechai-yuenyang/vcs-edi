# Generated by Django 4.2.5 on 2023-09-28 09:47

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="ManagementUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "avatar_url",
                    models.ImageField(upload_to="", verbose_name="Avatar Image"),
                ),
                (
                    "signature_img",
                    models.ImageField(upload_to="", verbose_name="Signature Image"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is Active"),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "ข้อมูล User",
                "verbose_name_plural": "User",
                "db_table": "tbmUser",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="PRIMARY KEY",
                    ),
                ),
                (
                    "code",
                    models.CharField(max_length=50, unique=True, verbose_name="Code"),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Name")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is Active"),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "ข้อมูล Department",
                "verbose_name_plural": "Department",
                "db_table": "tbmDepartment",
            },
        ),
        migrations.CreateModel(
            name="OrderType",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="PRIMARY KEY",
                    ),
                ),
                (
                    "code",
                    models.CharField(max_length=50, unique=True, verbose_name="Code"),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Name")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is Active"),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "ข้อมูล Order Type",
                "verbose_name_plural": "Order Type",
                "db_table": "tbmOrderType",
            },
        ),
        migrations.CreateModel(
            name="ProductGroup",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="PRIMARY KEY",
                    ),
                ),
                (
                    "code",
                    models.CharField(max_length=50, unique=True, verbose_name="Code"),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Name")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is Active"),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "ข้อมูล Product Group",
                "verbose_name_plural": "Product Group",
                "db_table": "tbmProductGroup",
            },
        ),
        migrations.CreateModel(
            name="ProductType",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="PRIMARY KEY",
                    ),
                ),
                (
                    "code",
                    models.CharField(max_length=50, unique=True, verbose_name="Code"),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Name")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is Active"),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "ข้อมูล Product Type",
                "verbose_name_plural": "Product Type",
                "db_table": "tbmProductType",
            },
        ),
        migrations.CreateModel(
            name="Section",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="PRIMARY KEY",
                    ),
                ),
                (
                    "code",
                    models.CharField(max_length=50, unique=True, verbose_name="Code"),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Name")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is Active"),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "ข้อมูล Section",
                "verbose_name_plural": "Section",
                "db_table": "tbmSection",
            },
        ),
        migrations.CreateModel(
            name="Unit",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="PRIMARY KEY",
                    ),
                ),
                (
                    "code",
                    models.CharField(max_length=50, unique=True, verbose_name="Code"),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Name")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is Active"),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "ข้อมูล Unit",
                "verbose_name_plural": "Unit",
                "db_table": "tbmUnit",
            },
        ),
        migrations.CreateModel(
            name="Supplier",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="PRIMARY KEY",
                    ),
                ),
                (
                    "code",
                    models.CharField(max_length=150, unique=True, verbose_name="Code"),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Name")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is Active"),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "user_id",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "ข้อมูล Supplier",
                "verbose_name_plural": "Supplier",
                "db_table": "tbmSupplier",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="PRIMARY KEY",
                    ),
                ),
                (
                    "code",
                    models.CharField(max_length=150, unique=True, verbose_name="Code"),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Name")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                ("img", models.ImageField(upload_to="", verbose_name="Image")),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is Active"),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "prod_group_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="supplier.productgroup",
                        verbose_name="Product Group ID",
                    ),
                ),
                (
                    "prod_type_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="supplier.producttype",
                        verbose_name="Product Type ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "ข้อมูล Product",
                "verbose_name_plural": "Product",
                "db_table": "tbmProduct",
            },
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="PRIMARY KEY",
                    ),
                ),
                (
                    "skid",
                    models.CharField(max_length=50, unique=True, verbose_name="Key"),
                ),
                ("code", models.CharField(max_length=50, verbose_name="Code")),
                ("name", models.CharField(max_length=250, verbose_name="Name")),
                ("prefix", models.CharField(max_length=250, verbose_name="Prefix")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is Active"),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "order_type_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="supplier.ordertype",
                        verbose_name="Type ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "ข้อมูล Book",
                "verbose_name_plural": "Book",
                "db_table": "tbmBook",
            },
        ),
        migrations.AddField(
            model_name="managementuser",
            name="department_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="supplier.department",
                verbose_name="Department ID",
            ),
        ),
        migrations.AddField(
            model_name="managementuser",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="managementuser",
            name="section_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="supplier.section",
                verbose_name="Section ID",
            ),
        ),
        migrations.AddField(
            model_name="managementuser",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
    ]
