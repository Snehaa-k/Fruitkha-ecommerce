# Generated by Django 5.0.1 on 2024-01-31 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="image",
            field=models.ImageField(upload_to="media"),
        ),
    ]
