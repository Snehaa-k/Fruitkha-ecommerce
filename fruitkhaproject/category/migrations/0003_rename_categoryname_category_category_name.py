# Generated by Django 5.0.1 on 2024-01-30 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0002_remove_category_description_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="category",
            old_name="categoryname",
            new_name="category_name",
        ),
    ]
