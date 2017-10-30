from django.http import HttpResponse
from django.shortcuts import render

from .fetch import xml


# Create your views here.
def leads(request, size):
    data = xml(int(size))
    return HttpResponse(data)
