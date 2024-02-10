from django.urls import path
from .views import UploadCreateView, upload

urlpatterns = [
    path('upload/', upload, name='upload'),
    path('upload-files/', UploadCreateView.as_view(), name='upload-files'),
]
