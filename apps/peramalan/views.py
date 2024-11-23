import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from openpyxl import load_workbook
from django.http import JsonResponse


# Decorators
from ..decorators import admin_required, guru_bk_required

# Form
from .forms import ExcelUploadForm, CenteroidForm

# Models Import
from django.contrib.auth.models import User

# Create your views here.


@admin_required
def index(request):
    form = ExcelUploadForm()
    CentForm = CenteroidForm()
    context = {
        "title": "K-Means & Elbow",
        "segment": "Clustering",
        "form": form,
        "centeroidForm": CentForm,
    }

    html_template = loader.get_template("page/peramalan.html")
    return HttpResponse(html_template.render(context, request))


def upload_excel(request):

    if request.method == "POST":
        file = request.FILES["file"]

        # Baca file Excel
        wb = load_workbook(file)
        sheet = wb.active  # Ambil sheet aktif
        data = []

        # Iterasi baris dan kolom
        for row in sheet.iter_rows(values_only=True):
            data.append(row)

        # Kembalikan data JSON
        return JsonResponse({"data": data})


def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))

def kmeans_step_by_step(request):
    
    context = {"form": ExcelUploadForm()}
    
    if request.method == "POST":
        file = request.FILES["file"]
       
        # Membuat DataFrame
        df = pd.read_excel(file)
        # Pastikan dataset memiliki kolom yang sesuai
        required_columns = ['Data 1', 'Data 2', 'Data 3']
        
        if not all(col in df.columns for col in required_columns):
            context['error'] = f"Dataset harus memiliki kolom: {', '.join(required_columns)}"
            return render(request, "page/kmeans_step.html", context)

        # Inisialisasi variabel untuk menyimpan langkah
        steps = []

        # Langkah 1: Inisialisasi centroid
        # Pilih kolom untuk clustering
        X = df[['Data 1', 'Data 2', 'Data 3']].to_numpy()

        # Manual K-Means untuk mencatat hasil per iterasi
        k = 3  # Jumlah kluster
        n_iter = 3 # Jumlah Iterasi
        np.random.seed(0)
        centroids = X[np.random.choice(X.shape[0], k, replace=False)]  # Inisialisasi centroid
        iteration_steps = []

        for iteration in range(n_iter):
            # Hitung jarak Euclidean
            distances = np.linalg.norm(X[:, None] - centroids[None, :, :], axis=2)
            clusters = np.argmin(distances, axis=1)

            # Catat langkah per iterasi
            step_data = {
                "iteration": iteration + 1,
                "count": k,
                "centroids": centroids.tolist(),
                "clusters": clusters.tolist(),
                "euclidean_distances": distances.tolist()
            }
            iteration_steps.append(step_data)

            # Update centroid
            new_centroids = np.array([X[clusters == i].mean(axis=0) if np.any(clusters == i) else centroids[i]
                                       for i in range(k)])
            if np.all(new_centroids == centroids):  # Jika tidak ada perubahan centroid, berhenti
                break
            centroids = new_centroids

        # Tambahkan hasil akhir ke DataFrame
        df['Kluster'] = clusters
        df['Euclidean Distance'] = [distances[i, clusters[i]] for i in range(len(X))]
        
        # Menampilkan hasil ke console
        print("\n=== Hasil K-Means Clustering ===")
        for step in iteration_steps:
            print(f"\n--- Iterasi {step['iteration']} ---")
            print("Centroids:", step['centroids'])
            print("Clusters:", step['clusters'])
            print("Euclidean Distances:", step['euclidean_distances'])
        # Kirim data langkah-langkah ke template
        return render(request, "page/kmeans_step.html", {"steps": iteration_steps})


def kmeans_step_by_step_2(request):
    
    context = {"form": ExcelUploadForm()}
    
    if request.method == "POST":
        file = request.FILES["file"]
       
        # Membuat DataFrame
        df = pd.read_excel(file)
        # Pastikan dataset memiliki kolom yang sesuai
        required_columns = ['Data 1', 'Data 2', 'Data 3']
        
        if not all(col in df.columns for col in required_columns):
            context['error'] = f"Dataset harus memiliki kolom: {', '.join(required_columns)}"
            return render(request, "page/kmeans_step.html", context)

        # Inisialisasi variabel untuk menyimpan langkah
        steps = []

        # Langkah 1: Inisialisasi centroid
        n_clusters = 3
        max_iter = 3
        X = df[['Data 1', 'Data 2', 'Data 3']]
        random_state = 0
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, init='random', n_init=1, max_iter=max_iter)
        kmeans.fit(X)
        centroids = kmeans.cluster_centers_

        steps.append({
            "step": "Inisialisasi centroid",
            "tags": "first",
            "count": n_clusters,
            "details": centroids.tolist(),
            "data": df.to_dict('records'),
            'distance': 'no'
        })
        
        print(centroids)
        # Iterasi clustering manual
        for i in range(max_iter):  # Maksimal 3 iterasi untuk demo
           
            # Hitung Euclidean Distance dari setiap siswa ke centroid
            distances_to_centroids = []
            for j in range(len(X)):
                distance = np.array([euclidean_distance(X.iloc[j], centroid) for centroid in centroids])
                distances_to_centroids.append(distance)

            df['Euclidean_Distances'] = distances_to_centroids

            steps.append({
                "step": f"Iterasi {i+1} - Hitung Euclidean Distances",
                "count": n_clusters,
                "data": df.to_dict('records'),
                'distance': 'yes'
            })
             # Langkah 2: Assign cluster
            labels = kmeans.predict(X)
            df['Kluster'] = labels
            df['Kluster'] += 1 
            
            steps.append({
                "step": f"Iterasi {i+1} - Hasil cluster",
                "details": df[['No', 'Kluster']].to_dict('records'),
                "data": df.to_dict('records'),
                'distance': 'no'
            })
            
            # Langkah 3: Update centroid
            centroids = df.groupby('Kluster').mean()[['Data 1', 'Data 2', 'Data 3']].values

            steps.append({
                "step": f"Iterasi {i+1} - Update centroid",
                "tags": "first",
                "count": n_clusters,
                "details": centroids.tolist(),
                "data": df.to_dict('records'),
                'distance': 'no'
            })
            # Update model dengan centroid baru
            kmeans.cluster_centers_ = centroids
            print(centroids)

        # Kirim data langkah-langkah ke template
        return render(request, "page/kmeans_step.html", {"steps": steps})
