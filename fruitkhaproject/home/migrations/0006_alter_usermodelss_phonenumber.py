# Generated by Django 5.0.1 on 2024-01-23 10:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_usermodelss_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodelss',
            name='phonenumber',
            field=models.BigIntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1000000000, message='Phone number must have at least 10 digits.'), django.core.validators.MaxValueValidator(limit_value=9999999999, message='Phone number must have at most 10 digits.')]),
        ),
    ]
