from django.core import serializers
from django.http import HttpResponse
# from django.shortcuts import render

from .models import Lead


# Create your views here.
def leads_xml(request, size):
    objs = Lead.objects.all()[:int(size)]
    data = serializers.serialize("xml", objs)
    return HttpResponse(data)


def leads_json(request, size):
    objs = Lead.objects.all()[:int(size)]
    data = serializers.serialize("json", objs)
    return HttpResponse(data)
