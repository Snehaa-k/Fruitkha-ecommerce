# Generated by Django 5.0.1 on 2024-01-22 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_usermodelss_is_verified_usermodelss_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodelss',
            name='phonenumber',
            field=models.BigIntegerField(),
        ),
    ]