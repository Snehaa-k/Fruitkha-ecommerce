# Generated by Django 5.0.1 on 2024-01-31 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_alter_products_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="description",
            field=models.TextField(max_length=500, unique=True),
        ),
    ]
