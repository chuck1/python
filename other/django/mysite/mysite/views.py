from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
import django.db.models
import django.views.generic

def home(request):
    #return django.http.HttpResponse(request, "Hello")
    return render(request, 'mysite/home.html', {})

