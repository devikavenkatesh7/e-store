# Generated by Django 5.0.3 on 2024-03-06 12:19

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Location",
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
                (
                    "phone",
                    models.CharField(
                        max_length=15,
                        validators=[
                            django.core.validators.RegexValidator("^[6-9]{1}\\d{9}$")
                        ],
                    ),
                ),
                ("address", models.TextField()),
                ("landmark", models.CharField(blank=True, max_length=45, null=True)),
                ("city", models.CharField(max_length=45)),
                (
                    "pincode",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(111111),
                            django.core.validators.MaxValueValidator(999999),
                        ]
                    ),
                ),
                ("state", models.CharField(max_length=45)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="locations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
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
                ("ordered_items", models.JSONField()),
                ("total_price", models.FloatField()),
                ("status", models.CharField(default="ordered", max_length=25)),
                ("ordered_date", models.DateTimeField(auto_now_add=True)),
                (
                    "delivery_address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="product.location",
                    ),
                ),
                (
                    "ordered_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderHistory",
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
                ("order", models.JSONField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("brand", models.CharField(max_length=45)),
                (
                    "price",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(99),
                            django.core.validators.MaxValueValidator(9999999),
                        ]
                    ),
                ),
                ("in_stock", models.IntegerField(default=0)),
                ("color", models.CharField(max_length=45)),
                (
                    "size",
                    models.CharField(
                        choices=[
                            ("XL", "XL"),
                            ("L", "L"),
                            ("XXL", "XXL"),
                            ("M", "M"),
                            ("S", "S"),
                        ],
                        max_length=5,
                    ),
                ),
                ("image", models.ImageField(upload_to="uploads/%Y/%M/%D")),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "added_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Cart",
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
                ("quantity", models.IntegerField(default=1)),
                ("is_purchased", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="product.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
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
                (
                    "profile_pic",
                    models.ImageField(blank=True, upload_to="profile_pics/"),
                ),
                ("dob", models.DateField(blank=True, null=True)),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
                        max_length=10,
                    ),
                ),
                ("place", models.CharField(blank=True, max_length=100)),
                ("recovery_email", models.EmailField(blank=True, max_length=254)),
                (
                    "mobile_number",
                    models.CharField(
                        blank=True,
                        max_length=15,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[6-9]\\d{9}$", "Invalid Indian mobile number"
                            )
                        ],
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Review",
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
                (
                    "rating",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
                ("comments", models.TextField()),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.product",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
