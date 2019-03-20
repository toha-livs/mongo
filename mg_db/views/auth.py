from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import redirect, render

from mg_db.models import Page


def login_test(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('test')
        return redirect('login')
    else:
        form = AuthenticationForm()
        return render(request, 'mg_db/login.html', {'form': form})


def logout_test(request):
    logout(request)
    return redirect('login')
