# Generated by Django 4.0.1 on 2022-12-11 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flat',
            old_name='type_id',
            new_name='type',
        ),
    ]