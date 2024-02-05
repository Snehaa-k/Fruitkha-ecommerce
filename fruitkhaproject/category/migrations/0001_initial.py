# Generated by Django 5.0.1 on 2024-01-24 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryname', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('is_listed', models.BooleanField(default=True)),
            ],
        ),
    ]
