# Generated by Django 5.0.1 on 2024-02-15 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0003_alter_orderdetails_product_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Coupon",
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
                ("cop_name", models.CharField(max_length=50)),
                ("cop_price", models.BigIntegerField()),
                ("code", models.CharField(max_length=50)),
                ("from_date", models.DateField()),
                ("to_date", models.DateField()),
                ("is_listed", models.BooleanField(default=True)),
            ],
        ),
    ]
