import os
from django import template
from django.core import serializers
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.conf import settings

#Decorators
from ..decorators import admin_required

# Models Import
from django.contrib.auth.models import User, Group
from ..models import m_data

# import class Form dari file forms.py
from .forms import PenggunaForm

# Create your views here.

@admin_required
def index(request):
    title = "Data Arsip"
    page = "Arsip"
    context = {"page": page, "title": title}

    html_template = loader.get_template("page/arsip.html")
    return HttpResponse(html_template.render(context, request))

# DESTROY
def delete(request, data_id):
    try:
        all_objs = m_data.objects.get(id=data_id)
        all_objs.delete()
        return redirect('arsip')
    except User.DoesNotExist:
        raise Http404("Task tidak ditemukan.")

# JSON DATA OBJECT
def json(request):
    if request.method == "GET":
        all_objs = m_data.objects.all().order_by('-id')
        # Serialize the data
        i=0
        data = {
        "data": [
            {
                "id": obj.id,
                "name": obj.data_name,
                "DT_RowIndex": i+1,
                "dataset": obj.dataset,  # Decode binary to string if needed
                "download_url": reverse('download_file', kwargs={"file_id": obj.id}),
                "created_at": obj.created_at.strftime("%d %B %Y"),
                "updated_at": obj.updated_at.strftime("%d %B %Y %H:%M"),
            }
            for i, obj in enumerate(all_objs)
        ]}
        return JsonResponse(data, safe=False)
    else:
        messages.error(request, 'Invalid Method')
        return redirect('arsip')

def download_file(request, file_id):
    obj = get_object_or_404(m_data, id=file_id)

    # Define the directory where the files are stored
    file_directory = os.path.join(settings.BASE_DIR, 'static', 'pdf')

    # Construct the full file path
    file_path = os.path.join(file_directory, obj.dataset)

    # Check if the file exists
    if os.path.exists(file_path):
        # Open the file in binary mode to read its contents
        with open(file_path, 'rb') as f:
            file_content = f.read()

        # Get the file extension from the file name (to determine MIME type)
        file_extension = file_path.split('.')[-1].lower()

        # Set appropriate content type for the file
        if file_extension == 'pdf':
            content_type = 'application/pdf'
        elif file_extension in ['jpg', 'jpeg']:
            content_type = 'image/jpeg'
        elif file_extension == 'png':
            content_type = 'image/png'
        else:
            content_type = 'application/octet-stream'

        # Create the HTTP response with the correct content type
        response = HttpResponse(file_content, content_type=content_type)

        # Set the content-disposition header with the custom filename
        response['Content-Disposition'] = f'attachment; filename="{obj.data_name}"'

        return response
    else:
        return HttpResponse("File not found.", status=404)