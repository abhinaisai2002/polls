from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import ProfileForm, RegisterForm,LoginForm
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from polls.models import *
# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('polls:allpolls')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            
            if form.is_valid():
                user = form.save(commit=False)

                email = request.POST.get('email')
                user.email = email
                user.save()
                send_mail(
                    'From PollPoller',
                    'Poll Poller welcomes you ',
                    'abhinaisai10@gmail.com',
                    [email],
                    fail_silently=True
                )
                username = form.cleaned_data.get('username')
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


@login_required(login_url='users:login')
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
        else:
            userpolls = Poll.objects.filter(creator=request.user)
            polls = []
            for i in range(0, len(userpolls), 2):
                try:
                    polls.append([userpolls[i], userpolls[i+1]])
                except:
                    polls.append([userpolls[i]])
            context = {
                'form': form,
                'polls': polls,
            }
            return  render(request, 'users/profile.html',context)
    else:
        form = ProfileForm(instance=request.user)


    userpolls = Poll.objects.filter(creator = request.user)
    polls = []
    for i in range(0,len(userpolls),2):
        try:
            polls.append([userpolls[i],userpolls[i+1]])
        except:
            polls.append([userpolls[i]]) 
    context = {
        'form': form,
        'polls':polls,
    }

    return render(request, 'users/profile.html', context)
