# Generated by Django 3.2.9 on 2022-01-21 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_rename_commision_commission'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commission',
            old_name='grand_total',
            new_name='order_price',
        ),
        migrations.RemoveField(
            model_name='commission',
            name='delivery_cost',
        ),
        migrations.RemoveField(
            model_name='commission',
            name='order_total',
        ),
    ]