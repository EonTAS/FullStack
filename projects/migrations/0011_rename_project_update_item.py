# Generated by Django 3.2.9 on 2022-02-04 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20220203_2246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='update',
            old_name='project',
            new_name='item',
        ),
    ]
