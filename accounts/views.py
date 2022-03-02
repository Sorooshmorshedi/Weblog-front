from base.models import Account
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate, forms
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

@csrf_exempt
def SignUpView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            login(request, user)
            return redirect('http://127.0.0.1:3000/profile/create' + '/?acid=' + str(user.id))
    elif request.method == 'GET':
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@csrf_exempt
def LoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            try:
                account = Account.objects.get(user=user.id)
                login(request, user)
                return redirect('http://127.0.0.1:3000/' + account.token + '/?acid=' + str(account.id))
            except:
                login(request, user)
                return redirect('http://127.0.0.1:3000/profile/create' + '/?acid=' + str(user.id))



    elif request.method == 'GET':
        form = AuthenticationForm()
    return render(request, 'accounts/base.html', {'form': form})

@csrf_exempt
def LogoutView(request):
    if request.method == 'GET':
        logout(request)
        return redirect('http://127.0.0.1:3000')
    elif request.method == 'POST':
        logout(request)
        return redirect('http://127.0.0.1:3000')

