# Generated by Django 5.0.1 on 2024-02-22 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]