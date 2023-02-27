
#Here I'm going to define my empty urlpatterns which is initially empty
#and we'll keep adding our patterns while building the application 

from django. urls import path 
from . import views

urlpatterns=[
#adding a url entry to patients/urls.py to associate the add_patiet route
#with the view as below
path('add_patient/',views.add_patient,name="add_patient"),
path('edit_patient/<str:patient_number>',views.edit_patient,name='edit_patient'),
path('', views.list_patients,name="list_patients"),
# path('identify_student',views.identify_student,name="identify_student"),
# path('identify_doctor',views.identify_doctor,name='identify_doctor'),
path('view_patient/<str:patient_number>',views.view_patient,name="view_patient"),
path('add_patient_record/<str:patient_number>',views.add_patient_record,name="add_patient_record"),
path('my_records/',views.my_records,name='my_records'),
path('doctor_info/',views.doctor_info, name='doctor_info'),
# path('create_patient',views.create_patient,name="create_patient"),
# path('identify_yourself',views.identify_yourself,name='identify_yourself')
]

