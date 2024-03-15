# Generated by Django 5.0.1 on 2024-02-14 10:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0002_orderdetails"),
        ("home", "0009_useraddress_delete_userprofile"),
        ("products", "0008_products_quantity_variant"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderdetails",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="products.products",
            ),
        ),
        migrations.AlterField(
            model_name="orderdetails",
            name="variant_units",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="products.variant",
            ),
        ),
        migrations.CreateModel(
            name="Orderditem",
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
                ("ex_deliverey", models.DateField()),
                ("status", models.CharField(max_length=50)),
                ("quantity", models.IntegerField()),
                ("order_number", models.IntegerField()),
                ("total_amount", models.IntegerField()),
                (
                    "address_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="home.useraddress",
                    ),
                ),
                (
                    "order_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cart.orderdetails",
                    ),
                ),
                (
                    "product_n",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.products",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.variant",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="home.usermodelss",
                    ),
                ),
            ],
        ),
    ]
