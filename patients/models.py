from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone


class School(models.Model):
    name = models.CharField("School name", max_length=120)
    address = models.CharField("School address", max_length=120)
    email = models.EmailField("School email", max_length=120)
    phone_number = models.CharField("School phone number", max_length=120, blank=True)

    # The string method generates a string representation of any Python object
    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField("Hospital name", max_length=120)
    address = models.CharField("Hospital address", max_length=120)
    email = models.EmailField("Hospital email", max_length=120)
    phone_number = models.CharField("Hospital phone number", max_length=120, blank=True)

    # The string method generates a string representation of any Python object
    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField("Doctor phone number", max_length=120, blank=True)
    hospital = models.ForeignKey(Hospital, null=True, blank=True, on_delete=models.CASCADE)
    licence_number = models.CharField("Proffesional Licence Number", max_length=10)

    def __str__(self):
        return f"{self.user.get_full_name()} {self.licence_number}"


class Patient(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField("Patient first name", max_length=120)
    last_name = models.CharField("Patient last name", max_length=120)
    date_of_birth = models.DateField()
    gender = models.CharField("Gender", max_length=10, choices=GENDER_CHOICES)
    
    patient_number = models.CharField("Patient number", max_length=120, unique=True)
    email = models.EmailField("Patient email", max_length=120)
    phone_number = models.CharField("Patient phone number", max_length=120, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    patient_status_on_admission = models.CharField(
        "patient status", max_length=120, default="Critical condition"
    )
    registered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patients_registered")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PatientRecord(models.Model):
    HIV_STATUS_CHOICES = (
        ('negative', 'Negative'),
        ('positive', 'Positive'),
        ('na', 'N/A'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="records")
    age = models.IntegerField("age")
    height = models.IntegerField("height")
    weight = models.IntegerField("weight")
    BG = models.CharField("Blood Group", max_length=120)
    BP = models.CharField("Blood Pressure Level", max_length=10)
    BMI = models.IntegerField("Body Mass Index")
    mother_name = models.CharField("Mother's Name ", max_length=120)
    mother_phone = models.CharField("Mother's Contact", max_length=13)
    father_name = models.CharField("Father's Name", max_length=120)
    father_phone = models.CharField("Father's Contact", max_length=13)
    Allergies = models.TextField("Allergies", max_length=255, default=None)
    vaccines_received = models.TextField("Vaccines received", max_length=100)
    hiv_status = models.CharField("HIV/AIDS", max_length=10, choices=HIV_STATUS_CHOICES)
    symptoms = models.TextField("Sypmtoms at the time of hospital visit")
    tests = models.TextField("Clinical Results and Tests done")
    diagnosis = models.TextField("Doctor's diagnosis")
    hospital = models.CharField("Hospital Name", max_length=255)
    prescription = models.TextField(
        "Treatment prescription",
    )
    progress_notes = models.TextField("Progress notes")
    created_at = models.DateTimeField("Date of records", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author}, {self.patient}"
