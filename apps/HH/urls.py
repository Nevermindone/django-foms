from django.urls import include, path
from django.views.generic import ListView
from .models import Queries
from apps.HH import views
from .views import *
from .views_folder.create_update_delete import *

urlpatterns = [
    path('', AddSkillsView.as_view(), name='add'),
    path('table/', table_create_view, name='table-list'),
    path('<int:pk>/update/', UpdateSkillsView.as_view(), name='update'),
    path('<int:pk>/delete/', DeleteSkillsView.as_view(), name='delete'),
    path('data/<int:id>/', request_data, name="data"),
]
