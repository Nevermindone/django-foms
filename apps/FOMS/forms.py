from django import forms

from apps.FOMS.models import File


class UploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']
