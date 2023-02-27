from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import PatientForm, DoctorForm, PatientRecordForm,StudentForm ,PatientSearchForm
from .models import Patient, Doctor, PatientRecord
from .utils import nicepass

# If a view function has the @login_required decorator,and an unauthenticated user
# tries to run it,Django will redirect the user to the login page
@login_required
def add_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.registered_by = request.user
            patient.save()
            user = User.objects.create(
                username=patient.patient_number,
                first_name=patient.first_name,
                last_name=patient.last_name,
                email=patient.email
            )
            password = nicepass()
            user.set_password(password)
            user.save()
            patient.user = user
            patient.save()
            messages.info(request, f"created user {user.username} with password {password}")
            return redirect("list_patients")
    else:
        form = PatientForm()

    return render(request, "add_patient.html", {"form": form})


@login_required
def edit_patient(request, patient_number):
    patient = get_object_or_404(patient_number=patient_number)
    if request.method == "POST":
        form = PatientRecordForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("list_patients")
    else:
        form = PatientForm(instance=patient)
        return render(request, "edit_patient.html", {"form": form})


@login_required
def list_patients(request):
    form = PatientSearchForm(request.GET)
    patients = Patient.objects.all()
    if form.is_valid():
        patient_number = form.cleaned_data["patient_number"]
        if patient_number:
            patients = patients.filter(patient_number__icontains=patient_number)
        first_name = form.cleaned_data["first_name"]
        if first_name:
            patients = patients.filter(first_name__icontains=first_name)
        last_name = form.cleaned_data["last_name"]
        if last_name:
            patients = patients.filter(last_name__icontains=last_name)

    return render(request, "list_patients.html", {"patients": patients, "form": form})


def view_patient(request, patient_number):
    patient = get_object_or_404(Patient, patient_number=patient_number)
    return render(request, "view_patient.html", {"patient": patient, "patient_records": patient.records.all()})


def my_records(request):
    patient = request.user.patient
    return render(request, "my_records.html", {"patient": patient, "patient_records": patient.records.all()})


def add_patient_record(request, patient_number):
    patient = get_object_or_404(Patient, patient_number=patient_number)
    if request.method == "POST":
        form = PatientRecordForm(request.POST)

        if form.is_valid():
            patient_record = form.save(commit=False)
            patient_record.patient = patient
            patient_record.author = request.user
            patient_record.save()
            return redirect("view_patient", patient_number=patient.patient_number)
    else:
        form = PatientRecordForm()
    return render(request, "add_patient_record.html", {"form": form, "patient": patient})


def doctor_info(request):
    if request.method == "POST":
        form = DoctorForm(request.POST, instance=request.user.doctor)
        print(form)
        if form.is_valid():
            form.save()
            return redirect("list_patients")
    else:
        form = DoctorForm(instance=request.user.doctor)
    return render(request, "doctor_info.html", {"form": form})




def student_info(request):
    form = StudentForm()
    return render(request, "student_info.html", {"form": form})


def identify_student(request):
    if request.method == "POST":
        return redirect("/student_info")


def identify_doctor(request):
    if request.method == "POST":
        return redirect("/doctor_info")


def identify_yourself(request):
    return redirect("identify_yourself.html")


""" #checking if the requested patient exists in the database
            firstname=request.POST.get('firstname')
            lastname=request.POST.get('lastname')
            patient_no=request.POST.get('patient_no')
            patient=PatientRecordsModel.objects.filter(firstname=firstname,lastname=lastname,patient_no=patient_no)
            if patient:
                data=PatientRecordsModel.objects.get()

            form.save()
            """

"""def assign_patient_id():
    patientid=random.randint(0,1000)
    alphanumeric_id="P{:2023d}".format(patientid)
    return alphanumeric_id

def create_patient_records(request):

    print("storing Patient data")

    if request.method=="POST":
        form=PatientRecordsForm (request.POST)
        print(form)
        if form.is_valid():
            cleaned_data= form.cleaned_data
            form.save()
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        alpha_numeric_id=assign_patient_id()
        patient=PatientRecordsModel.objects.create(firstname=firstname,lastname=lastname,patient_no=alpha_numeric_id)
        
        
def get_records(request):

    firstname=request.POST.get('firstname')
    lastname=request.POST.get('lastname')
    patient_id=request.POST.get('patient_no')
    patient=PatientRecordsModel.objects.filter(firstname=firstname,lastname=lastname,patient_no=patient_id)
    #return patient.objects.all()
    if request.method=="GET":
        for field in ["firstname","lastname","patient_no"]:
            name=request.GET[field]
            return render(request, "add_patient.html",{"doctor":name,"schools":["Buddo","SMACK","Gayaza","Namagunga"]})   
    #validating the data by checking if first_name, last_name and patient_no are empty
    #if any of them are empty,we redisplay the form with the already entered message 
    #informing the user that they need to fill in the empty values.
    context={}
    if request.method == "POST":
        entered_data={}
        for field in ["firstname","lastname","patient_no"]:
            #populate context with entered value which will be redisplayed in case 
            #the form is invalid
            entered_data[field]=request.POST[field]
            print(entered_data)
            value=request.POST[field]
            print(value)
            if not value:
                context["error_message"]=f"Please fill in the {field}"
                print(context)
        if "error_message" in context:
            #update context with entered data
            context.update(entered_data)
            print(context)
    else:
        pass

    #render() is a utility function provided by django that generates a response 
    #from the html file passed as the second argument in this case add_patient.html
    return render(request, "add_patient.html",context=context)
"""
