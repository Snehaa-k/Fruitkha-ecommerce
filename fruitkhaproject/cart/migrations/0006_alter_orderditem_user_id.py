# Generated by Django 5.0.1 on 2024-02-15 13:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_proceedtocheck'),
        ('home', '0009_useraddress_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderditem',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.usermodelss'),
        ),
    ]
