# Generated by Django 4.2 on 2023-04-09 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='zip_code',
            new_name='zipcode',
        ),
    ]
