# Generated by Django 2.0.2 on 2020-06-11 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_cart', '0002_cartinfo_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartinfo',
            name='total',
        ),
    ]
