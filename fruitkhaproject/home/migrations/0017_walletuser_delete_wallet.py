# Generated by Django 5.0.1 on 2024-02-22 05:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0016_alter_wallet_amount"),
    ]

    operations = [
        migrations.CreateModel(
            name="Walletuser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amountt", models.ImageField(default=0, upload_to="")),
                (
                    "userid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="home.usermodelss",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Wallet",
        ),
    ]
