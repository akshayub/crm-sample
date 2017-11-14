from django.core import serializers
from django.http import HttpResponse
# from django.shortcuts import render

from .models import *


# Create your views here.
def leads_xml(request, size):
    objs = Lead.objects.all()[:int(size)]
    data = serializers.serialize("xml", objs)
    return HttpResponse(data)


def leads_json(request, size):
    objs = Lead.objects.all()[:int(size)]
    data = serializers.serialize("json", objs)
    return HttpResponse(data)


def accounts(request, dtype, start, end):
    objs = Account.objects.all()[int(start):int(end)]
    if dtype == 'json':
        data = serializers.serialize('json', objs)
    else:
        data = serializers.serialize('xml', objs)
    return HttpResponse(data)


def contacts(request, dtype, start, end):
    objs = Contact.objects.all()[int(start):int(end)]
    if dtype == 'json':
        data = serializers.serialize('json', objs)
    else:
        data = serializers.serialize('xml', objs)
    return HttpResponse(data)


def leads(request, dtype, start, end):
    objs = Lead.objects.all()[int(start):int(end)]
    if dtype == 'json':
        data = serializers.serialize('json', objs)
    else:
        data = serializers.serialize('xml', objs)
    return HttpResponse(data)


def opportunities(request, dtype, start, end):
    objs = Opportunity.objects.all()[int(start):int(end)]
    if dtype == 'json':
        data = serializers.serialize('json', objs)
    else:
        data = serializers.serialize('xml', objs)
    return HttpResponse(data)


def update_lead(request, lid, status):
    ld = Lead.objects.get(id=lid)
    ld.status = status
    ld.save()
    return HttpResponse('OK')


def update_oppo(request, oid, stage):
    ld = Opportunity.objects.get(id=oid)
    ld.stage = stage
    if stage == '5':
        ld.probability = '0'
    else:
        ld.probability = 100 // (5 - int(stage))
    ld.save()
    return HttpResponse('OK')
