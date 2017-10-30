from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, JsonResponse
import json
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


def chart1(request):
    """
    var chartData = {
            labels: [10, 100, 1000],
            datasets: [{
                label: 'JSON',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255,99,132,1)',
                data: [1, 9.73, 100],
                yAxisID: 'first-y-axis'
            },{
                label: 'XML',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                data: [2, 24, 150],
                yAxisID: 'first-y-axis'
            }]
        };
    """

    full_url = HttpRequest.build_absolute_uri(request)
    relative = HttpRequest.get_full_path(request)

    base_url = full_url[:-len(relative)]

    # TODO: Find a better way to write this part of the code. Please forgive me for this part.. :(

    json_10_url = reverse('objects:leads_json', args=['10'])
    json_100_url = reverse('objects:leads_json', args=['100'])
    json_1000_url = reverse('objects:leads_json', args=['1000'])

    xml_10_url = reverse('objects:leads_xml', args=['10'])
    xml_100_url = reverse('objects:leads_xml', args=['100'])
    xml_1000_url = reverse('objects:leads_xml', args=['1000'])

    json10 = requests.get(base_url + json_10_url).elapsed.microseconds
    json100 = requests.get(base_url + json_100_url).elapsed.microseconds
    json1000 = requests.get(base_url + json_1000_url).elapsed.microseconds

    xml10 = requests.get(base_url + xml_10_url).elapsed.microseconds
    xml100 = requests.get(base_url + xml_100_url).elapsed.microseconds
    xml1000 = requests.get(base_url + xml_1000_url).elapsed.microseconds

    json_data = [json10, json100, json1000]
    xml_data = [xml10, xml100, xml1000]

    final_data = {
        'labels': [10, 100, 1000],
        'datasets': [
            {
                'label': 'JSON',
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'borderColor': 'rgba(255,99,132,1)',
                'data': json_data,
                'yAxisID': 'first-y-axis'
            },
            {
                'label': 'XML',
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'data': xml_data,
                'yAxisID': 'first-y-axis'
            }
        ]
    }

    # data_in_json = json.dumps(final_data)
    # print(data_in_json)
    return JsonResponse(final_data)
