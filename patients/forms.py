from django import forms
from .models import Patient, School, Doctor, PatientRecord


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient  # here I'm associating the model and  the form
        exclude = ["user", "registered_by", "created_at"]
        widgets = {
            'date_of_birth': forms.SelectDateWidget,
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor  # here I'm associating the model and  the form
        exclude = ["created_at", "user"]


class PatientRecordForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        exclude = ["created_at", "author", "patient"]


class PatientSearchForm(forms.Form):
    patient_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Patient No.'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
