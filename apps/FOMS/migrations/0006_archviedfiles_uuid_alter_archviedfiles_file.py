# Generated by Django 5.0.2 on 2024-02-21 18:40

import apps.FOMS.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FOMS', '0005_rename_batch_id_archviedfiles_batch'),
    ]

    operations = [
        migrations.AddField(
            model_name='archviedfiles',
            name='uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='archviedfiles',
            name='file',
            field=models.FileField(upload_to=apps.FOMS.models.get_upload_path),
        ),
    ]
