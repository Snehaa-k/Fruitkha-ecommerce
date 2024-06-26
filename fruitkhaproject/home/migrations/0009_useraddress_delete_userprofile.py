# Generated by Django 5.0.1 on 2024-02-10 09:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0008_userprofile"),
    ]

    operations = [
        migrations.CreateModel(
            name="Useraddress",
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
                ("Name", models.CharField(max_length=225)),
                ("country", models.CharField(max_length=200)),
                ("state", models.CharField(max_length=200)),
                ("address", models.TextField()),
                ("pin", models.BigIntegerField()),
                ("post", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.BigIntegerField()),
                ("is_cancelled", models.BooleanField(default=False)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="home.usermodelss",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Userprofile",
        ),
    ]
