# Generated by Django 5.0.1 on 2024-02-26 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0011_categoryoffer_productoffer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="categoryoffer",
            name="percentage",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="productoffer",
            name="percentage",
            field=models.IntegerField(),
        ),
    ]
