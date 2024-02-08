from django.db import models


class BatchUpload(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    archives_count = models.IntegerField(blank=True, null=True)


class ArchviedFiles(models.Model):
    name = models.CharField(blank=True, null=True)
    file = models.FileField(upload_to='uploads/')
    batch = models.ForeignKey(to=BatchUpload, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
