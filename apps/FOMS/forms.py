from django import forms

from apps.FOMS.models import ArchviedFiles


class UploadForm(forms.ModelForm):
    class Meta:
        model = ArchviedFiles
        fields = ['file']
