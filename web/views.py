from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


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
