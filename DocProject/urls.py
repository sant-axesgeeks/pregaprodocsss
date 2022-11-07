from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('register/doctor', views.DoctorRegister, name='doctorregister'),
    path('doctor_sent_otp',login.as_view(),name='login'),
    path('doctor_verify_otp/<str:phone_number>',verify_otp.as_view(),name='verify_otp'),
    
    path('register/patient', views.PatientRegister, name='patientregister'),
    
    
    path('login/', UserLoginView.as_view(), name='login'),
    path('subscribe/<str:id>', views.subscribe, name='subscribe'),
    
    path('patient_profile/<str:id>',views.patient_profile,name='patient_profile'),
    path('edit_patient_profile/<str:id>',views.edit_patient_profile),

    path('appointment/<str:id>', views.appointment, name='appointment'),
    
    path('patient_appointment_detail/<str:id>', views.patient_appointment_details, name='patient_appointment_detail'),
    
    path('doctor_profile', views.doctor_profile, name='doctor_profile'),
    path('edit_doctor_profile/<str:id>',views.edit_doctor_profile),
    path('doctor_profile_by_id/<str:id>', views.doctor_profile_by_id, name='doctor_profile_by_id'),
    
    path('doctor_appointment_detail/<str:id>', views.doctor_appointment_details, name='doctor_appointment_detail'),
    
    path('medicalcouncil',views.list_of_medical_council,name='medicalcouncil'),
    
   # path('iscompletedpatient/<str:id>',views.patient_appointmentcompleted,name='iscompleted'),
    
    path('iscompleteddoctor/<str:id>',views.doctor_appointmentcompleted,name='iscompleted'),
    
    #path('completedappointment/<str:patient_appointment_id>/<str:doctor_appointment_id>',views.completed_appointment,name='completed_appointment'),
    path("get_completed_appointment/<str:id>",views.get_completed_appointment,name='get_completed_appointment'),
    path('current_appointment/<str:id>',views.current_appointment,name='current_appointment'),
    
    path('askquery/<str:id>',views.askquery,name='askquery'),
    
    path('answer_query/<str:id>',views.answer_query,name='answer_query'),
    path('list_of_queries/<str:id>',views.list_of_queries,name='list_of_queries'),  

    #path('baby/<str:s>',views.baby,name='baby'),
    path('babyname',views.babyname,name='baby'),

    #wallet
    path('recievemoney/<str:id>',views.recieve_money,name='recievemoney'),
    path('withdrawmoney/<str:id>',views.withdraw_money,name='withdrawmoney'),
    path('transactionhistory/<str:id>',views.transactionhistory,name='transactionhistory'),

    #blog
    path('blog/<str:id>',views.blog,name='blog'),
    path('list_of_blogs/<str:id>',views.list_of_blogs,name='list_of_blogs'),
    
    path('yearly_graph/<str:id>',views.yearly_graph_of_appointments,name='graphs'),
   # path('monthly_graph/<str:id>',views.monthly_graph_of_appointments,name='graphs'),
    
]