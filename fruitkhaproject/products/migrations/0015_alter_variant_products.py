# Generated by Django 5.0.1 on 2024-03-01 04:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0014_alter_categoryoffer_category_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="variant",
            name="products",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="variant",
                to="products.products",
            ),
        ),
    ]
