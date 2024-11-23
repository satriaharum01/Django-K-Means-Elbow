from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('peramalan/', views.index, name='peramalan'),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
    path('kmeans-steps/', views.kmeans_step_by_step, name='kmeans_steps'),
    path('elbow_plot/', views.elbow_plot, name='elbow_plot'),
]

# Menyajikan file media saat dalam mode pengembangan
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)