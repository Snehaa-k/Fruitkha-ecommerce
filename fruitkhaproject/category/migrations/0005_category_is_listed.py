# Generated by Django 5.0.1 on 2024-02-03 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_alter_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_listed',
            field=models.BooleanField(default=True),
        ),
    ]
