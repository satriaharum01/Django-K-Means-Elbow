from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
    
class m_data(models.Model):
    id = models.IntegerField(primary_key=True, max_length=11)
    data_name = models.CharField(max_length=100)
    dataset = models.CharField(max_length=250)  # Mediumblob (binary field for storing file content)
    c_type = models.CharField(
        max_length=10,
        choices=[('average', 'Average'), ('random', 'Random')],
        default='random'
    )  # Enum-like choices
    n_cluster = models.IntegerField()  # Number of clusters
    n_iter = models.IntegerField()  # Number of iterations
    s_elbow = models.IntegerField()  # Start elbow
    e_elbow = models.IntegerField()  # End elbow
    n_elbow_iter = models.IntegerField()  # Number of elbow iterations
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update on save

    def __str__(self):
        return f"ClusteringData(id={self.id}, type={self.c_type})"
    
    class Meta:
        db_table = 'data_history'
        

class m_centeroid(models.Model):
    
    TYPES = [
        ('average', 'Rata-rata nilai'),
        ('random', 'Random Centeroid'),
    ]
    
    centeroid_type = models.CharField(max_length=20, choices=TYPES, default='random')
    jumlah_cluster = models.IntegerField()  
    max_perulangan = models.IntegerField()  
    
    def __str__(self):
        return f"{self.jumlah_cluster}({self.get_centeroid_type_display()})"
    