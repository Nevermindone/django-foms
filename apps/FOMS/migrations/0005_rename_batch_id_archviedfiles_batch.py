# Generated by Django 5.0.2 on 2024-02-08 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FOMS', '0004_batchupload_archviedfiles_batch_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='archviedfiles',
            old_name='batch_id',
            new_name='batch',
        ),
    ]
