from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import RegisterForm,LoginForm
from django.contrib import messages
# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('polls:allpolls')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = request.user.username
                messages.success(request,f"Account created for {username}")
                return redirect('users:login')
        else:
            form = RegisterForm()
        context = {
            'form' : form
        }
    return render(request,'users/register.html',context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('polls:allpolls')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('polls:allpolls')
            else:
                form = LoginForm(data=request.POST)
                return render(request,'users/login.html',{'form':form})

        else:
            form  = LoginForm()
            context = {
                'form' : form
            }
    return render(request,'users/login.html',context)

def logout_view(request):
    logout(request)
    return redirect('users:login')