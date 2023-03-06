from django.contrib import admin

from .models import Doctor, Patient, PatientRecord, School, Hospital,LisenceNumber


admin.site.register(School)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(PatientRecord)
admin.site.register(Hospital)
admin.site.register(LisenceNumber)