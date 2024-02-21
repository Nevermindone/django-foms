import os

from django.db import models
import uuid


def get_upload_path(instance, filename):
    return os.path.join(
      "uploads", str(instance.batch.id), str(filename)
    )


class BatchUpload(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    archives_count = models.IntegerField(blank=True, null=True)


class ArchviedFiles(models.Model):
    name = models.CharField(blank=True, null=True)
    file = models.FileField(upload_to=get_upload_path)
    batch = models.ForeignKey(to=BatchUpload, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
