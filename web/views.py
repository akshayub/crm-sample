from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, JsonResponse
import time
import requests

from objects.models import *
from .forms import AccountForm, ContactForm, LeadForm, OppoForm


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'web/login.html')
    else:
        return render(request, 'web/home.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('web:index')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('web:index')
            else:
                return render(request, 'web/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'web/login.html', {'error_message': 'Invalid login'})
    return render(request, 'web/login.html')


def logout_user(request):
    logout(request)
    return render(request, 'web/login.html')


def compare(request):
    if not request.user.is_authenticated:
        return render(request, 'web/login.html')
    return render(request, 'web/compare.html')


def accounts(request):
    if not request.user.is_authenticated:
        return render(request, 'web/login.html')
    return render(request, 'web/accounts.html')


def account(request, aid):
    if not request.user.is_authenticated:
        return render(request, 'web/login.html')
    try:
        r = Account.objects.get(id=aid)
    except ObjectDoesNotExist:
        error_message = "The Account with that ID does not exists"
        return render(request, 'web/account.html', {'error_message': error_message})

    ctcs = Contact.objects.filter(works_for=r.id)
    oppo = Opportunity.objects.filter(account=r.id)
    loc = AccountLocation.objects.filter(account=r.id)

    if len(ctcs) == 0:
        ctcs = None

    if len(oppo) == 0:
        oppo = None

    if len(loc) == 0:
        loc = None

    data = {
        'id': r.id,
        'name': r.name,
        'phone': r.phone_number,
        'website': r.website,
        'parent': r.subsidiary_of,
        'contacts': ctcs,
        'opportunities': oppo,
        'locations': loc,
        'owner': r.owner.user.first_name + " " + r.owner.user.last_name
    }

    return render(request, 'web/account.html', data)


def account_create(request):
    if not request.user.is_authenticated:
        return render(request, 'web/login.html')
    form = AccountForm(request.POST or None)
    if form.is_valid():
        acct = form.save(commit=False)
        acct.owner = Owner.objects.get(user=request.user)
        acct.save()
        return render(request, 'web/accounts.html')
    context = {
        "form": form,
    }
    return render(request, 'web/account_create.html', context)


def account_update(request, aid):
    if not request.user.is_authenticated:
        return render(request, 'web/login.html')
    form = AccountForm(request.POST or None, instance=Account.objects.get(id=aid))
    if form.is_valid() and request.POST:
        acct = form.save(commit=False)
        acct.owner = Owner.objects.get(user=request.user)
        acct.save()
        return render(request, 'web/accounts.html')
    context = {
        "form": form,
    }
    return render(request, 'web/account_edit.html', context)


def contact_create(request):
    if not request.user.is_authenticated:
        return render(request, 'web/login.html')
    form = ContactForm(request.POST or None)
    if form.is_valid():
        cntct = form.save(commit=False)
        cntct.owner = Owner.objects.get(user=request.user)
        cntct.save()
        return render(request, 'web/contacts.html')
    context = {
        "form": form,
    }
    return render(request, 'web/contact_create.html', context)


def contacts(request):
    if not request.user.is_authenticated:
        return render(request, 'web/login.html')
    return render(request, 'web/contacts.html')


def contact(request, cid):
    if not request.user.is_authenticated:
        return render(request, 'web/login.html')
    try:
        r = Contact.objects.get(id=cid)
    except ObjectDoesNotExist:
        error_message = "The contact with that ID does not exists"
        return render(request, 'web/contact.html', {'error_message': error_message})

    data = {
        'id': r.id,
        'name': r.name,
        'phone': r.phone_number,
        'address': r.address,
        'email': r.email,
        'bdate': r.bdate,
        'added_on': r.added_on,
        'works_for': r.works_for,
        'owner': r.owner
    }

    return render(request, 'web/contact.html', data)


def contact_update(request, cid):
    if not request.user.is_authenticated:
        return render(request, 'web/login.html')
    form = ContactForm(request.POST or None, instance=Contact.objects.get(id=cid))
    if form.is_valid() and request.POST:
        acct = form.save(commit=False)
        acct.owner = Owner.objects.get(user=request.user)
        acct.save()
        return render(request, 'web/contacts.html')
    context = {
        "form": form,
    }
    return render(request, 'web/contact_edit.html', context)


def lead(request, lid):
    try:
        r = Lead.objects.get(id=lid)
    except ObjectDoesNotExist:
        error_message = "The Lead with that ID does not exists"
        return render(request, 'web/lead.html', {'error_message': error_message})

    data = {
        'id': r.id,
        'name': r.name,
        'address': r.address,
        'company': r.company,
        'email': r.email,
        'status': r.status,
        'added_on': r.added_on,
        'amount': r.amount,
        'owner': r.owner
    }

    return render(request, 'web/lead.html', data)


def leads(request):
    if not request.user.is_authenticated:
        return render(request, 'web/login.html')
    return render(request, 'web/leads.html')


def lead_create(request):
    if not request.user.is_authenticated:
        return render(request, 'web/login.html')
    form = LeadForm(request.POST or None)
    if form.is_valid():
        ld = form.save(commit=False)
        ld.owner = Owner.objects.get(user=request.user)
        ld.save()
        return render(request, 'web/leads.html')
    context = {
        "form": form,
    }
    return render(request, 'web/lead_create.html', context)


def lead_update(request, lid):
    if not request.user.is_authenticated:
        return render(request, 'web/login.html')
    form = LeadForm(request.POST or None, instance=Lead.objects.get(id=lid))
    if form.is_valid() and request.POST:
        acct = form.save(commit=False)
        acct.owner = Owner.objects.get(user=request.user)
        acct.save()
        return render(request, 'web/leads.html')
    context = {
        "form": form,
    }
    return render(request, 'web/lead_edit.html', context)


def opportunity(request, oid):
    if not request.user.is_authenticated:
        return render(request, 'web/login.html')
    try:
        r = Opportunity.objects.get(id=oid)
    except ObjectDoesNotExist:
        error_message = "The Opportunities with that ID does not exist"
        return render(request, 'web/opportunity.html', {'error_message': error_message})

    data = {
        'id': r.id,
        'name': r.name,
        'stage': r.stage,
        'account': r.account,
        'close_date': r.close_date,
        'probability': r.probability,
        'amount': r.amount,
        'description': r.description,
    }

    return render(request, 'web/opportunity.html', data)


def opportunities(request):
    if not request.user.is_authenticated:
        return render(request, 'web/login.html')
    return render(request, 'web/opportunities.html')


def opportunity_create(request):
    if not request.user.is_authenticated:
        return render(request, 'web/login.html')
    form = OppoForm(request.POST or None)
    if form.is_valid():
        ld = form.save(commit=False)
        ld.owner = Owner.objects.get(user=request.user)
        ld.save()
        return render(request, 'web/opportunities.html')
    context = {
        "form": form,
    }
    return render(request, 'web/opportunity_create.html', context)


def opportunity_update(request, oid):
    if not request.user.is_authenticated:
        return render(request, 'web/login.html')
    form = OppoForm(request.POST or None, instance=Opportunity.objects.get(id=oid))
    if form.is_valid() and request.POST:
        acct = form.save(commit=False)
        acct.owner = Owner.objects.get(user=request.user)
        acct.save()
        return render(request, 'web/opportunities.html')
    context = {
        "form": form,
    }
    return render(request, 'web/opportunity_edit.html', context)


def chart1(request):
    """
    This view tests the server speed for transferring JSON and XML objects.

    :param request: The AJAX request
    :return: JsonResponse of the dataset.
    """

    full_url = HttpRequest.build_absolute_uri(request)
    relative = HttpRequest.get_full_path(request)

    base_url = full_url[:-len(relative)]

    request_amount = ['10', '100', '200', '500', '1000']

    json_urls = list()
    xml_urls = list()

    for x in request_amount:
        json_urls.append(reverse('objects:leads_json', args=[x]))
        xml_urls.append(reverse('objects:leads_xml', args=[x]))

    json_data = list()
    xml_data = list()

    for x in json_urls:
        start = time.perf_counter()
        requests.get(base_url + x)
        end = time.perf_counter()
        json_data.append((end - start))

    for x in xml_urls:
        start = time.perf_counter()
        requests.get(base_url + x)
        end = time.perf_counter()
        xml_data.append((end - start))

    final_data = {
        'labels': request_amount,
        'datasets': [
            {
                'label': 'JSON',
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'borderColor': 'rgba(255,99,132,1)',
                'data': json_data,
                'borderWidth': 2,
                'yAxisID': 'first-y-axis'
            },
            {
                'label': 'XML',
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'data': xml_data,
                'borderWidth': 2,
                'yAxisID': 'first-y-axis'
            }
        ]
    }

    return JsonResponse(final_data)


def chart2(request):
    """
    This view returns the JSON and XML test data for client resolving test
    :param request: The AJAX request
    :return: JsonResponse of the JSON and XML
    """
    full_url = HttpRequest.build_absolute_uri(request)
    relative = HttpRequest.get_full_path(request)

    base_url = full_url[:-len(relative)]

    request_amount = ['10', '100', '200', '500', '1000']

    json_content = list()
    xml_content = list()

    for x in request_amount:
        json_content.append(requests.get(base_url + reverse('objects:leads_json', args=[x])).text)
        xml_content.append(requests.get(base_url + reverse('objects:leads_xml', args=[x])).text)

    response = {
        'json': json_content,
        'xml': xml_content
    }

    return JsonResponse(response)


def chart3(request):
    full_url = HttpRequest.build_absolute_uri(request)
    relative = HttpRequest.get_full_path(request)

    base_url = full_url[:-len(relative)]

    request_amount = ['10', '100', '200', '500', '1000']

    json_content = list()
    xml_content = list()

    for x in request_amount:
        json_content.append(len(requests.get(base_url + reverse('objects:leads_json', args=[x])).text)/1024)
        xml_content.append(len(requests.get(base_url + reverse('objects:leads_xml', args=[x])).text)/1024)

    response = {
        'json': json_content,
        'xml': xml_content
    }

    return JsonResponse(response)
