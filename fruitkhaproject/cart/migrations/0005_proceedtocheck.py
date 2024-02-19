# Generated by Django 5.0.1 on 2024-02-15 06:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_coupon'),
        ('home', '0009_useraddress_delete_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proceedtocheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField()),
                ('total_amount', models.BigIntegerField(default=0)),
                ('discount_amount', models.BigIntegerField(null=True)),
                ('is_coupenapplyed', models.BooleanField(default=False)),
                ('applyed_coupen', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.coupon')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.usermodelss')),
            ],
        ),
    ]