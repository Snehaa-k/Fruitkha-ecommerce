# Generated by Django 5.0.1 on 2024-02-17 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0012_wishlist_vaiant_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="wishlist",
            name="vaiant_id",
        ),
    ]
