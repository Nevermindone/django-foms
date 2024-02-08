from django.db import models


class File(models.Model):
    name = models.CharField(blank=True, null=True)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.name
