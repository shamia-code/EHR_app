from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout

from .forms import LoginForm, RegisterForm
from patients.models import Doctor

def sign_in(request):
    if request.method=='POST':
        form=LoginForm(request.POST)

        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            #The authenticate() function verifies a username and password to see if they are 
            #valid and returns an instance of the User class or None otherwise 
            user=authenticate(request, username=username, password=password)
            if user:
                login(request,user)#this login function creates a session id on the server and sends it back to the web browser in the form of a cookie 
                try:
                    doc = user.doctor
                    return redirect("list_patients")
                except Doctor.DoesNotExist:
                    return redirect("my_records")
    else: 
        form=LoginForm()
    return render(request,'login.html',{'form':form})

def sign_out(request):
    logout(request)
    return redirect('login')
    
def sign_up(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)#creating an instance of the RegisterForm 
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            Doctor.objects.create(
                user=user,
                licence_number=user.username
            )
            login(request,user)
            return redirect('list_patients')
    else:
        form=RegisterForm()
    return render(request,'register.html',{'form':form})
