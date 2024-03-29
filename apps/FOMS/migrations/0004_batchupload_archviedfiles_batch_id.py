# Generated by Django 5.0.2 on 2024-02-08 02:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FOMS', '0003_rename_file_archviedfiles'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('archives_count', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='archviedfiles',
            name='batch_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='FOMS.batchupload'),
            preserve_default=False,
        ),
    ]
