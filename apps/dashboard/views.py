import os
from django import template
from django.core import serializers
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Models Import
from django.contrib.auth.models import User
from ..models import m_data
from ..decorators import admin_required

# Create your views here.
@login_required
@admin_required
def index(request):
    data = {}
    context = {"segment": "dashboard","value": data}

    html_template = loader.get_template("page/dashboard.html")
    return HttpResponse(html_template.render(context, request))
