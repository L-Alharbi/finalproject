from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm 
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def loginPage(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, passsword=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            None

    context = {}
    return render(request, 'store/login.html', context)


def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form':form}
    return render(request, 'store/register.html', context)




def store(request):
    products = Product.objects.all()
    context = {'products' :products}
    return render(request, 'store/store.html', context)

def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)
