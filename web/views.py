from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, JsonResponse
import time
import requests


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
    return render(request, 'web/compare.html')


def accounts(request):
    return render(request, 'web/accounts.html')


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
        req = requests.get(base_url + x)
        end = time.perf_counter()
        json_data.append((end - start))

    for x in xml_urls:
        start = time.perf_counter()
        req = requests.get(base_url + x)
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
