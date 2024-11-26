from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('peramalan/', views.index, name='peramalan'),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
    path('kmeans-steps/', views.kmeans_step_by_step, name='kmeans_steps'),
    path('clustering_view/', views.clustering_view, name='clustering_view'),
    path('summary/', views.summary, name='summary'),
]

# Menyajikan file media saat dalam mode pengembangan
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)