from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout

from .forms import LoginForm, RegisterForm
from patients.models import Doctor,LisenceNumber

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
        doctor=LisenceNumber.objects.all()
        if form.is_valid():
            licence=form.cleaned_data['username']
            if licence:
                doctor=doctor.filter(licence_number__icontains=licence)
            first_name=form.cleaned_data['first_name']
            if first_name:
                doctor=doctor.filter(first_name__icontains=first_name)
            last_name=form.cleaned_data['last_name']
            if last_name:
                doctor=doctor.filter(last_name__icontains=last_name)
                print("{} is a reqistered doctor, access ganted!" .format(doctor))
                
                return redirect("list_patients")
        
        else:
            print("Not a registered doctor!")
            form=RegisterForm()
            return render(request,'register.html',{'form':form})
            """
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            Doctor.objects.create(
                user=user,
                    licence_number=user.username
                )
                login(request,user)
                return redirect('register.html')
        """
    else:
        form=RegisterForm()
    return render(request,'register.html',{'form':form})
