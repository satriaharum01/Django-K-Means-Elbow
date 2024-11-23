from django.urls import path, re_path
from . import views

urlpatterns = [
    path('arsip/', views.index, name='arsip'),
    path('arsip/save', views.create, name='arsip/save'),
    path('arsip/update/<int:data_id>', views.update, name="arsip/update"),
    path('arsip/delete/<int:data_id>', views.delete, name="arsip/delete"),
    path('arsip/json', views.json, name="arsip/json"),
    path('arsip/find/<int:data_id>', views.find, name="arsip/find"),
]
