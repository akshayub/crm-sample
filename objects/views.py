from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
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
    objs = Account.objects.order_by('-added_on')[int(start):int(end)]
    if dtype == 'json':
        data = serializers.serialize('json', objs)
    else:
        data = serializers.serialize('xml', objs)
    return HttpResponse(data)


def contacts(request, dtype, start, end):
    objs = Contact.objects.order_by('-added_on')[int(start):int(end)]
    if dtype == 'json':
        data = serializers.serialize('json', objs)
    else:
        data = serializers.serialize('xml', objs)
    return HttpResponse(data)


def leads(request, dtype, start, end):
    objs = Lead.objects.order_by('-added_on')[int(start):int(end)]
    if dtype == 'json':
        data = serializers.serialize('json', objs)
    else:
        data = serializers.serialize('xml', objs)
    return HttpResponse(data)


def opportunities(request, dtype, start, end):
    objs = Opportunity.objects.order_by('-close_date')[int(start):int(end)]
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


def account_delete(request, aid):
    rec = Account.objects.get(id=aid).delete()
    return HttpResponse("OK")


def contact_delete(request, cid):
    rec = Contact.objects.get(id=cid).delete()
    return HttpResponse("OK")


def lead_delete(request, lid):
    rec = Lead.objects.get(id=lid).delete()
    return HttpResponse("OK")


def oppo_delete(request, oid):
    rec = Opportunity.objects.get(id=oid).delete()
    return HttpResponse("OK")


def account_search(request):
    search = request.GET.get('q', '')
    recs = Account.objects.filter(name__icontains=search)
    data = serializers.serialize('json', recs)
    return HttpResponse(data)


def contact_search(request):
    search = request.GET.get('q', '')
    recs = Contact.objects.filter(name__icontains=search)
    data = serializers.serialize('json', recs)
    return HttpResponse(data)


def lead_search(request):
    search = request.GET.get('q', '')
    recs = Lead.objects.filter(name__icontains=search)
    data = serializers.serialize('json', recs)
    return HttpResponse(data)


def oppo_search(request):
    search = request.GET.get('q', '')
    recs = Opportunity.objects.filter(name__icontains=search)
    data = serializers.serialize('json', recs)
    return HttpResponse(data)


def dashboard_lead_data(request):
    r_not_closed = Lead.objects.filter(status__lt=3).aggregate(Sum('amount'))['amount__sum']
    r_not_converted = Lead.objects.filter(status=3).aggregate(Sum('amount'))['amount__sum']
    r_converted = Lead.objects.filter(status=4).aggregate(Sum('amount'))['amount__sum']

    data = {
        'datasets': [{
            'data': [r_not_closed, r_not_converted, r_converted],
            "backgroundColor": ["rgb(255, 99, 132)", "rgb(54, 162, 235)", "rgb(255, 205, 86)"]
        }],
        'labels': ['Not Closed', 'Not converted', 'Converted']
    }

    return JsonResponse(data)


def dashboard_oppo_data(request):
    r_not_closed = Opportunity.objects.filter(stage__lt=4).aggregate(Sum('amount'))['amount__sum']
    r_not_converted = Opportunity.objects.filter(stage=5).aggregate(Sum('amount'))['amount__sum']
    r_converted = Opportunity.objects.filter(stage=4).aggregate(Sum('amount'))['amount__sum']

    data = {
        'datasets': [{
            'data': [r_not_closed, r_not_converted, r_converted],
            "backgroundColor": ["rgb(157, 147, 101)", "rgb(54, 162, 235)", "rgb(25, 5, 206)"]
        }],
        'labels': ['Not Closed', 'Closed Lost', 'Closed Won']
    }

    return JsonResponse(data)


def recent_unclosed_leads(request):
    rew = Lead.objects.filter(status__lt=3).order_by('-added_on')[:10]
    data = serializers.serialize('json', rew)
    return JsonResponse(data, safe=False)


def lead_to_acc(request, lid):
    obj = Lead.objects.get(id=lid)
    name = obj.name
    address = obj.address
    company = obj.company
    email = obj.email
    acct = Account.objects.create(
        name=company,
        owner=Owner.objects.get(user=request.user)
    )

    ctc = Contact.objects.create(
        name=name,
        address=address,
        email=email,
        bdate=now(),
        owner=Owner.objects.get(user=request.user),
        works_for=acct
    )
    return HttpResponse('OK')
