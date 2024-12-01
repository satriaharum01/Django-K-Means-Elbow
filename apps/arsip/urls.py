from django.urls import path, re_path
from . import views

urlpatterns = [
    path('arsip/', views.index, name='arsip'),
    path('arsip/delete/<int:data_id>', views.delete, name="arsip/delete"),
    path('arsip/json', views.json, name="arsip/json"),
    path('arsip/download/<int:file_id>', views.download_file, name='download_file'),
]
