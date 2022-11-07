
from turtle import title

from yaml import serialize
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

import jwt
import requests
import json
from time import time

API_KEY = 'Npls_v9uRSqn0RJda8ruZQ'
API_SEC = 'q4ywKxgjb6yvq1LdPqbxYlP9mUlIEOE48h9S'
def generateToken():
    token = jwt.encode(
  
        # Create a payload of the token containing
        # API Key & expiration time
        {'iss': API_KEY, 'exp': time() + 5000},
  
        # Secret used to generate token signature
        API_SEC,
  
        # Specify the hashing alg
        algorithm='HS256'
    )
    print(token)
    return token
meetingdetails = {"topic": "The title of your zoom meeting",
                  "type": 2,
                  "start_time": "2019-06-14T10: 21: 57",
                  "duration": "45",
                  "timezone": "Asia/Calcutta",
                  "agenda": "test",
  
                  "recurrence": {"type": 1,
                                 "repeat_interval": 1
                                 },
                  "settings": {"host_video": "true",
                               "participant_video": "True",
                               "join_before_host": "True",
                               "mute_upon_entry": "False",
                               "watermark": "true",
                               "audio": "voip",
                               "auto_recording": "cloud"
                               }
                  }
  

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


@api_view(['POST'])
def DoctorRegister(request):

  try:
    if request.method == 'POST':
      # import pdb
      # pdb.set_trace()
      email = request.data['email']
      password = request.data['password']
      password2 = request.data['password2']
      name = request.data['name']
      if name == '':
        return Response({'message': 'Name is required'})
      qualification = request.data['qualification']
      if qualification == '':
        return Response({"message": "Qualification is required"})
      profession = request.data['profession']
      if profession == '':
        return Response({"message": "Profession is required"})
      upload_id = request.FILES.get('upload_id')
      if upload_id == '':
        return Response({'message': 'Upload ID is required'})
      experience = request.data['experience']
      if experience == '':
        return Response({'message': 'Experience is required'})
      working_location1 = request.data['working_location1']
      if working_location1 == '':
        return Response({'message': 'Working Location is required'})
      longitude_1 = request.data['longitude_1']
      if longitude_1 == '':
        return Response({'message': 'Longitude is required'})
      latitude_1 = request.data['longitude_1']
      if latitude_1 == '':
        return Response({'message': 'Latitude is required'})
      working_location2 = request.data['working_location2']
      working_location2_img = request.data['working_location2_img']
      
      working_location3 = request.data['working_location3']
      working_location3_img = request.data['working_location3_img']
      
      working_location4 = request.data['working_location4']
      working_location4_img = request.data['working_location4_img']
      working_location5 = request.data['working_location5']
      working_location5_img = request.data['working_location5_img']
      
      doc_img = request.FILES.get('doc_img')
      if doc_img == '':
        return Response({'message': 'Doctor Image is required'})
      phone_number = request.data['phone_number']
      if phone_number == '':
        return Response({'message': 'Phone Number is required'})
      
      if password != password2:
        return Response({"msg":"Password and Confirm Password doesn't match"})
      try:
        if (User.objects.get(email=email)is not None) and (Doctor.objects.get (phone_number=phone_number)is not None):
          return Response({"msg":"email or phone number already exists"})
      except:
        user = User.objects.create_user(email=email, password=password)
        user.save()
        user1 = User.objects.get(email=email)
        token = get_tokens_for_user(user)

        doctor = Doctor.objects.create(user=user1, name=name,profession=profession,upload_id=upload_id,working_location1=working_location1,working_location2=working_location2,working_location3=working_location3,working_location4=working_location4,working_location5=working_location5,qualification=qualification,experience=experience,doc_img=doc_img, phone_number=phone_number,longitude_1=longitude_1,latitude_1=latitude_1,working_location2_img=working_location2_img,working_location3_img=working_location3_img,working_location4_img=working_location4_img,working_location5_img=working_location5_img)
        Wallet.objects.create(doctor_id=doctor,amount=0,total_amount=0)

        return Response({"phone_number":phone_number,'token':token,'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
  except:
    return Response({"msg":"Registration Failed"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_profile_by_id(request,id):
  try:
    if request.method == 'GET':
  
      
      doctor_id=Doctor.objects.get(id = id) 
      json_data={"id":doctor_id.id,
      "email":doctor_id.user.email,                  
      "name":doctor_id.name,
      "profession":doctor_id.profession,
      "working_location":doctor_id.working_location,
      "qualification":doctor_id.qualification,
      'upload_id':str(request.build_absolute_uri(doctor_id.upload_id.url)),
      "experience":doctor_id.experience,
      "doc_img":str(request.build_absolute_uri(doctor_id.doc_img.url)),
      "phone_number":doctor_id.phone_number,
      }
      
    return Response({"data":json_data}, status=status.HTTP_200_OK)
  except:
    return Response({"msg":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
#@permission_classes([IsAuthenticated])
def edit_doctor_profile(request,id):
  try:
    if request.method == 'PUT':
 
      cs = Doctor.objects.get(id=id)
      profession = request.data['profession']
      working_location = request.data['working_location']
      qualification = request.data['qualification']
      experience = request.data['experience']
      Doctor.objects.update(profession=profession,working_location=working_location,qualification = qualification,experience = experience,)
      return Response({"email":cs.user.email,"name":cs.name,"profession":profession,"working_location":working_location,"qualification":qualification,"experience":experience,"phone_number":cs.phone_number,"msg":"profile updated successfully",'upload_id':str(request.build_absolute_uri(cs.upload_id.url)),"doc_img":str(request.build_absolute_uri(cs.doc_img.url))})
  except:
    return Response({"msg":"Something is wrong"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_appointment_details(request,id):
  try:
    if request.method == "GET":
      doctor_id=Doctor.objects.get(id = id)
      ap = DocAppointment.objects.filter(doctor_id=doctor_id)
      json_data2 = []
      for k in ap:
          json_data2.append({"patient_id":k.patient_id.id,"email":k.patient_id.user.email,"name":k.patient_id.name,"age":k.patient_id.age,"phone_number":k.patient_id.phone_number,"appointment_url":k.appointment_url,"appointment_date":k.appointment_date,"appointment_time":k.appointment_time,})
      return Response({"data":json_data2}, status=status.HTTP_200_OK)
  except:
    return Response({"data":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)  

@api_view(['POST'])
def PatientRegister(request):
  try:
    if request.method == 'POST':
      
      con_or_preg_type = request.data['con_or_preg_type']
      email = request.data['email']
      password = request.data['password']
      password2 = request.data['password2']
      age = request.data['age']
      if age == '':
        return Response({'message': 'Age is required'})
      name = request.data['name']
      if name == '':
        return Response({'message': 'Name is required'})
      
      phone_number = request.data['phone_number']
      if phone_number == '':
        return Response({'message': 'Phone Number is required'})
      
      if password != password2:
        return Response({"msg":"Password and Confirm Password doesn't match"})
      
      try:
        if (User.objects.get(email=email)is not None) and (Patient.objects.get (phone_number=phone_number)is not None):
          return Response({"msg":"email or phone number already exists"})
      except:
        user = User.objects.create_user(email=email, password=password)
        user.save()
        token = get_tokens_for_user(user)
        user1 = User.objects.get(email=email)
        patient = Patient.objects.create(user=user1,con_or_preg_type=con_or_preg_type, name=name,age=age,phone_number=phone_number)
        return Response({'patient_id':patient.id,"name":name,"email":email,"phone_number":phone_number,'msg':'Registration Successful','token':token,}, status=status.HTTP_201_CREATED)
  except:
    return Response({"msg":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)

class UserLoginView(APIView):
  serializer_class = UserLoginSerializer
  def post(self, request, format=None):
    try:
      serializer = UserLoginSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      email = serializer.data.get('email')
      password = serializer.data.get('password')
      user = authenticate(email=email, password=password)
      try:
        if Patient.objects.get(user=user):
          patient_id = Patient.objects.get(user=user)
          subs = subscription.objects.filter(patient_id=patient_id)
          if user is not None:
            token = get_tokens_for_user(user)
            return Response({"con_or_preg_type":patient_id.con_or_preg_type,"id":patient_id.id,'token':token, 'msg':'Login Success',"packages":[{"package":x.package} for x in subs]}, status=status.HTTP_200_OK)
          else:
            return Response({"msg":'Email or Password is not Valid'}, status=status.HTTP_404_NOT_FOUND)
      except:
        if Doctor.objects.get(user=user):
          doctor_id = Doctor.objects.get(user=user)
          if user is not None:
            token = get_tokens_for_user(user)
            return Response({"id":doctor_id.id,'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
          else:
            return Response({"msg":'Email or Password is not Valid'}, status=status.HTTP_404_NOT_FOUND)
    except:
      return Response({"msg":'Email or Password is not Valid'}, status=status.HTTP_404_NOT_FOUND)

import os
from twilio.rest import Client
def send_otp(phone_number,otp):
  url = "https://www.fast2sms.com/dev/bulkV2"
  authkey = settings.AUTH_KEY
  querystring = {"authorization":authkey,"route":otp,"numbers":phone_number}

  headers = {
      'cache-control': "no-cache"
  }

  response = requests.request("GET", url, headers=headers, params=querystring)

  print(response.text)
#   # Download the helper library from https://www.twilio.com/docs/python/install



# # Find your Account SID and Auth Token at twilio.com/console
# # and set the environment variables. See http://twil.io/secure
#   account_sid = os.environ['TWILIO_ACCOUNT_SID']
#   auth_token = os.environ['TWILIO_AUTH_TOKEN']
#   client = Client(account_sid, auth_token)

#   message = client.messages \
#                   .create(
#                       body="Your OTP is "+otp,
#                       from_='+17473195376',
#                       to=phone_number
#                   )

#   print(message.sid)


#user login with otp
import random
from django.http import JsonResponse
class login(APIView):
  serializer_class = Login_Serializer
  def post(self,request):
    try:
    
      phone_number = request.data['phone_number']
      data = Doctor.objects.get(phone_number=phone_number)
      
      if data is not None:
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
          otp = str(random.randint(1000, 9999))
          Doctor.objects.update(otp = otp)
          
          send_otp(phone_number,otp)
          return JsonResponse({"otp":otp,"msg":"otp sent"}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"message": "Not sent"}, status=status.HTTP_400_BAD_REQUEST)
    except:
      return JsonResponse({"message": "Not sent"}, status=status.HTTP_400_BAD_REQUEST)

class verify_otp(APIView):
  serializer_class = Verify_Serializer
  def post(self,request,phone_number):
    try:
      serializer = self.serializer_class(data=request.data)
      if serializer.is_valid(raise_exception=True):
        otp = request.data['otp']
        user = Doctor.objects.get(phone_number=phone_number)
        authenticate(user)
        if user.otp == otp:
          token = get_tokens_for_user(user)
          
          return Response({"id":user.id,'token':token, 'msg':'Loggedin Successfully'}, status=status.HTTP_200_OK)
        else:
          return JsonResponse({"msg":"otp not verified"}, status=status.HTTP_400_BAD_REQUEST)
      else:
        return JsonResponse({"msg":"otp not verified"}, status=status.HTTP_400_BAD_REQUEST)
    except:
      return Response({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe(request,id):
 
  patient = Patient.objects.get(id=id)
  if request.method == 'POST':
    razorpay_payment_id = request.data['razorpay_payment_id']
    amount = request.data['amount']
    package = request.data['package']
    subscription.objects.create(package=package,razorpay_payment_id=razorpay_payment_id,amount = amount)
    return Response({"name":patient.name,"email":patient.user.email,"phone_number":patient.phone_number,"razorpay_payment_id":razorpay_payment_id,"package":package,'msg':'Subscription Successful'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_profile(request,id):
  try:
    if request.method == 'GET':
      
      patient_id=Patient.objects.get(id=id)
      json_data={"id":patient_id.id,
                    "email":patient_id.user.email,
                    "name":patient_id.name,
                    "age":patient_id.age,
                    "phone_number":patient_id.phone_number,
                    }
      return Response({"data":json_data}, status=status.HTTP_200_OK)
  except:
    return Response({"data":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
#@permission_classes([permission_classes])
def edit_patient_profile(request,id):
  try:
  
    if request.method == "PUT":
      ds = Patient.objects.get(id=id)
      con_or_preg_type = request.data['con_or_preg_type']
      age = request.data['age']
      name = request.data['name']
      Patient.objects.update(con_or_preg_type=con_or_preg_type,age = age,name = name)
      return Response ({"email":ds.user.email,"con_or_preg_type":con_or_preg_type,"age":age,"name":name,"phone_number":ds.phone_number,"msg":"profile succesfully updated"})
  except:
    return Response({"msg":"something is wrong"})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_appointment_details(request,id):
  try:
    if request.method == 'GET':
      patient_id=Patient.objects.get(id=id)
      ap = Appointment.objects.filter(patient_id=patient_id)
      json_data= []
      for k in ap:
        json_data.append({"doctor_id":k.doctor_id.id,
                                    "email":k.doctor_id.user.email,
                                    "name":k.doctor_id.name,
                                    "profession":k.doctor_id.profession,
                                    "qualification":k.doctor_id.qualification,
                                    "upload_id":str(request.build_absolute_uri(k.doctor_id.upload_id.url)),
                                    "working_location":k.doctor_id.working_location,
                                    "experience":k.doctor_id.experience,
                                    "doc_img":str(request.build_absolute_uri(k.doctor_id.doc_img.url)),
                                    "phone_number":k.doctor_id.phone_number,"appointment_url":k.appointment_url,"appointment_date":k.appointment_date,"appointment_time":k.appointment_time})
      return Response({"data":json_data}, status=status.HTTP_200_OK)
  except:
    return Response({"data":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_of_medical_council(request):
  try:
    if request.method == 'GET':
      json_data = []
      states = MedicalCouncil.objects.all()
      for i in states:
        json_data.append({"1":i.state1,"2":i.state2,"3":i.state3,"4":i.state4,"5":i.state5,"6":i.state6,"7":i.state7,"8":i.state8,"9":i.state9,"10":i.state10,"11":i.state11,"12":i.state12,"13":i.state13,"14":i.state14,"15":i.state15,"16":i.state16,"17":i.state17,"18":i.state18,"19":i.state19,"20":i.state20,"21":i.state21,"22":i.state22,"23":i.state23,"24":i.state24,"25":i.state25,"26":i.state26,"27":i.state27,"28":i.state28,"29":i.state29,"30":i.state30})
      return Response ({'data':json_data},status=status.HTTP_200_OK)
  except:
    return Response({"data":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_profile(request):
  try:
    if request.method == 'GET':
      import pdb 
      pdb.set_trace()
      json_data = []
      # json_data2 = []
      doctor_id=Doctor.objects.all()
      for i in doctor_id:
        ap = Appointment.objects.filter(doctor_id=i.id)
        json_data.append({"id":i.id,
        "email":i.user.email,
        "name":i.name,
        "profession":i.profession,
        "qualification":i.qualification,
        'upload_id':(str(request.build_absolute_uri(i.upload_id.url))) if i.upload_id else None,
        'working_location1':i.working_location1,
        'working_location2':i.working_location2,
        'working_location3':i.working_location3,
        'working_location4':i.working_location4,
        'working_location5':i.working_location5,
        'working_location2_img':(str(request.build_absolute_uri(i.working_location2_img.url))) if i.working_location2_img else None,
        'working_location3_img':(str(request.build_absolute_uri(i.working_location3_img.url))) if i.working_location3_img else None,
        'working_location4_img':(str(request.build_absolute_uri(i.working_location4_img.url))) if i.working_location4_img else None,
        'working_location5_img':(str(request.build_absolute_uri(i.working_location5_img.url))) if i.working_location5_img else None,
        "experience":i.experience,
        "doc_img":(str(request.build_absolute_uri(i.doc_img.url))) if i.doc_img else None,
        "phone_number":i.phone_number,
        "appointments":[{"appointment_date":k.appointment_date,"appointment_time":k.appointment_time,"doctor_name":k.doctor_id.name,"appointment_url":k.appointment_url,"doctor_profession":k.doctor_id.profession,"doctor_experience":k.doctor_id.experience} for k in ap],
        })
        
    return Response({"data":json_data}, status=status.HTTP_200_OK)

  except:
    return Response({"data":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def appointment(request,id):
  try:
    if request.method == 'POST':
      patient_id=Patient.objects.get(id=id)
      headers = {'authorization': 'Bearer ' + generateToken(),
                  'content-type': 'application/json'}
      r = requests.post(
            f'https://api.zoom.us/v2/users/me/meetings',
            headers=headers, data=json.dumps(meetingdetails))
      
      y = json.loads(r.text)
      join_URL = y["join_url"]
      meetingPassword = y["password"]
      
      doctor_id = request.data['doctor_id']
      appointment_date = request.data['appointment_date']
      appointment_time= request.data['appointment_time']
      doctor = Doctor.objects.get(id=doctor_id)
      appointment_patient = Appointment.objects.create(doctor_id=doctor, patient_id=patient_id,appointment_date=appointment_date,appointment_time=appointment_time,appointment_url=join_URL,url_password=meetingPassword)

      appointment_doctor=DocAppointment.objects.create(doctor_id=doctor, patient_id=patient_id,appointment_date=appointment_date,appointment_time=appointment_time,appointment_url=join_URL,url_password=meetingPassword)
      json_data={"patient_appointment_id":appointment_patient.id,"doctor_appointment_id":appointment_doctor.id,"appointment_url":appointment_patient.appointment_url,"zoom_password":appointment_patient.url_password,'msg':'Appointment Created'}

      
      return Response({"data":json_data}, status=status.HTTP_201_CREATED)
  except:
    return Response({"data":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def patient_appointmentcompleted(request,id):
#   try:
#     if request.method == 'POST':
#       ds = Appointment.objects.get(id=id)
#       ispatientcompleted = request.data['ispatientcompleted']
#       Appointment.objects.update(ispatientcompleted=ispatientcompleted)
#       return Response({'msg':'Appointment Completed'}, status=status.HTTP_200_OK)
#   except:
#     return Response({"msg":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)
  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def doctor_appointmentcompleted(request,id):
  try:
    if request.method == 'POST':
      ds = DocAppointment.objects.get(id=id)
      isdoctorcompleted = request.data['isdoctorcompleted']
      DocAppointment.objects.update(isdoctorcompleted=isdoctorcompleted)
      cs = Appointment.objects.get(id=id)
      ps = DocAppointment.objects.get(id=id)
      if ps.isdoctorcompleted == True:
        CompletedAppointment.objects.create(patient_id=ps.patient_id,doctor_id=ps.doctor_id,appointment_url = ps.appointment_url,appointment_date=ps.appointment_date,appointment_time=ps.appointment_time)
        ps.delete()
        cs.delete()
        return Response({'msg':'Appointment Completed'}, status=status.HTTP_200_OK)
      elif ps.isdoctorcompleted == False:
        CompletedAppointment.objects.create(patient_id=ps.patient_id,doctor_id=ps.doctor_id,appointment_url = ps.appointment_url,appointment_date=ps.appointment_date,appointment_time=ps.appointment_time)
        ps.delete()
        cs.delete()
        return Response({'msg':'Appointment Completed'}, status=status.HTTP_200_OK)
  except:
    return Response({"msg":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def completed_appointment(request,patient_appointment_id,doctor_appointment_id):
#   try:
#     if request.method == 'POST':
#       ps = Appointment.objects.get(id=patient_appointment_id)
#       ds = DocAppointment.objects.get(id=doctor_appointment_id)
#       if ps.ispatientcompleted == True and ds.isdoctorcompleted == True:
#         CompletedAppointment.objects.create(patient_id=ps.patient_id,doctor_id=ps.doctor_id,appointment_url = ps.appointment_url,appointment_date=ps.appointment_date)
#         ps.delete()
#         ds.delete()
#         return Response({'msg':'Appointment Completed'}, status=status.HTTP_200_OK)
#       elif ps.ispatientcompleted == True and ds.isdoctorcompleted == False:
#         CompletedAppointment.objects.create(patient_id=ps.patient_id,doctor_id=ps.doctor_id,appointment_url = ps.appointment_url,appointment_date=ps.appointment_date)
#         ps.delete()
#         ds.delete()
#         return Response({'msg':'Doctor was not there'}, status=status.HTTP_200_OK)
#       elif ps.ispatientcompleted == False and ds.isdoctorcompleted == True:
#         CompletedAppointment.objects.create(patient_id=ps.patient_id,doctor_id=ps.doctor_id,appointment_url = ps.appointment_url,appointment_date=ps.appointment_date)
#         ps.delete()
#         ds.delete()
#         return Response({'msg':'Patient was not there'}, status=status.HTTP_200_OK)
#   except:
#     return Response({"msg":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_completed_appointment(request,id):
  try:
    if request.method == 'GET':
      cs = Doctor.objects.get(id=id)
      ps = CompletedAppointment.objects.filter(doctor_id=cs)
      json_data=[]
      for k in ps:
        json_data.append({
          "patient_name":k.patient_id.name,
          "appointment_date":k.appointment_date,
          "appointment_time":k.appointment_time,
          "appointment_url":k.appointment_url,
        })
      return Response({"data":json_data}, status=status.HTTP_200_OK)
  except:
    return Response({"data":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)
  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def askquery(request,id):
  try:
    if request.method == 'POST':
      qs = Patient.objects.get(id=id)
      doctor_id=request.data['doctor_id']
      query = request.data['query']
      doctor = Doctor.objects.get(id=doctor_id)
      cs =AskQuery.objects.create(patient_id=qs,doctor_id=doctor,query=query)
      return Response({"query_id":cs.id,'query':query,"msg":"Query recieved by doctor"}, status=status.HTTP_200_OK)
  except:
    return Response({"msg":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND) 

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def answer_query(request,id):
  try:
    if request.method == 'POST':
      qs = AskQuery.objects.get(id=id)
      answer = request.data['answer']
      AskQuery.objects.update(answer=answer)
      return Response({"query":qs.query,"answer":answer,'msg':'Answer Given'}, status=status.HTTP_200_OK)
  except:
    return Response({"msg":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)
import datetime  

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_of_queries(request,id):
  try:
    if request.method == 'GET':
      ks = Doctor.objects.get(id=id)
      ss = AskQuery.objects.filter(doctor_id=ks)
      json_data = []
      for k in ss:
        json_data.append({"patient_id":k.patient_id.id,"patient_name":k.patient_id.name,"query":k.query,"answer":k.answer,"query_id":k.id})
      return Response({"data":json_data}, status=status.HTTP_200_OK)
  except:
    return Response({"data":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_appointment(request,id):
  try:
    if request.method == 'GET':
      doctor_id = Doctor.objects.get(id=id)
      ps = DocAppointment.objects.filter(doctor_id=doctor_id,appointment_date=datetime.datetime.now().date())
      json_data=[]
      for k in ps:
        json_data.append({
          "patient_name":k.patient_id.name,
          "appointment_date":k.appointment_date,
          "appointment_time":k.appointment_time,
          "appointment_url":k.appointment_url,
        })
      return Response({"data":json_data}, status=status.HTTP_200_OK)
  except:
    return Response({"data":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)


# def baby(request,s):
#   url = "https://baby-names2.p.rapidapi.com/names/"+str(s)

#   headers = {
#     "X-RapidAPI-Key": "a7db1f6365msh0a3b019878f2506p1bbe0fjsn09beffcdbd72",
#     "X-RapidAPI-Host": "baby-names2.p.rapidapi.com"
#   }

#   response = requests.request("GET", url, headers=headers)
#   ss = response.json()
#   for i in ss:
#       BabyName.objects.create(name=i['name'])

@api_view(['POST'])
def babyname(request):
  try:
    name = request.data['name']
    if request.method == 'POST':
      ks = BabyName.objects.filter(name__startswith=name)
      json_data=[]
      for k in ks:
        json_data.append({"name":k.name})
      return Response({"data":json_data}, status=status.HTTP_200_OK)
  except:
    return Response({"data":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recieve_money(request,id):
  
  try:
    if request.method == 'POST':
     
      ks = Doctor.objects.get(id=id)
      cs = Wallet.objects.get(doctor_id=ks)
      transaction_id = request.data['transaction_id']
      amount = request.data['amount']
      description = request.data['description']
      if amount > 0:
        kd = cs.total_amount+amount
        Wallet.objects.update(total_amount=kd)
        print(kd)
        Transaction.objects.create(amount=amount,description=description,doctor_id=ks,transaction_type='credit',transaction_id=transaction_id)
        return Response({"total_amount":kd,"msg":"Money Transfered"}, status=status.HTTP_200_OK)

      else:
        return Response({"msg":"Amount is not valid"}, status=status.HTTP_200_OK)
  except:
    return Response({"msg":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw_money(request,id):
  try:
    if request.method == 'POST':
      ks = Doctor.objects.get(id=id)
      cs = Wallet.objects.get(doctor_id=ks)
      amount = request.data['amount']
      description = request.data['description']
      transaction_id = request.data['transaction_id']
      if amount > 0:
        if cs.total_amount >= amount:
          kd = cs.total_amount-amount
          Wallet.objects.update(total_amount=kd)
          print(kd)
          Transaction.objects.create(amount=amount,description=description,doctor_id=ks,transaction_type="Withdraw",transaction_id=transaction_id)
          return Response({"total_amount":kd,"msg":"Amount deducted"}, status=status.HTTP_200_OK)
        else:
          return Response({"msg":"Amount is not valid"}, status=status.HTTP_200_OK)
  except:
    return Response({"msg":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transactionhistory(request,id):
  try:
    if request.method == 'GET':
      ks = Doctor.objects.get(id=id)
      ss = Transaction.objects.filter(doctor_id=ks)
      json_data = []
      for k in ss:
        json_data.append({"amount":k.amount,"description":k.description,"transaction_type":k.transaction_type,"transaction_id":k.transaction_id,"name":k.doctor_id.name,"email":k.doctor_id.user.email,"phone_number":k.doctor_id.phone_number})
      return Response({"data":json_data}, status=status.HTTP_200_OK)
  except:
    return Response({"data":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def blog(request,id):
  try:
    if request.method == 'POST':
      ks = Doctor.objects.get(id=id)
      title = request.data['title']
      content = request.data['content']
      Blog.objects.create(doctor_id = ks,title=title,content=content)
      return Response({"msg":"Blog Added"}, status=status.HTTP_200_OK)
  except:
    return Response({"msg":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_of_blogs(request,id):
  try:
    if request.method == 'GET':
      ks = Doctor.objects.get(id=id)
      ss = Blog.objects.filter(doctor_id=ks)
      json_data = []
      for k in ss:
        json_data.append({"title":k.title,"content":k.content,"name":k.doctor_id.name,"email":k.doctor_id.user.email,"phone_number":k.doctor_id.phone_number})
      return Response({"data":json_data}, status=status.HTTP_200_OK)
  except:
    return Response({"data":"Something is wrong"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def yearly_graph_of_appointments(request,id):
  if request.method == 'GET':
    ks = Doctor.objects.get(id=id)
    ss = Appointment.objects.filter(doctor_id=ks).dates('appointment_date','year')
    json_data = []
    for k in ss:
      ps = Appointment.objects.filter(doctor_id=ks).filter(appointment_date__year=k.year)
      

      json_data.append({"year":k.year,"Appointments":len(ps)})
      
    return Response({"data":json_data}, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def monthly_graph_of_appointments(request,id):
#   if request.method == 'GET':
#     ks = Doctor.objects.get(id=id)
#     cs =Appointment.objects.filter(doctor_id=ks).dates('appointment_date','month')
#     json_data = []
#     for k in cs:
#       ps = Appointment.objects.filter(doctor_id=ks).filter(appointment_date__year=k.year,appointment_date__month=k.month)
      
#       json_data.append({k.year:{str(k.month):len(ps)}})
#     return Response({"data":json_data}, status=status.HTTP_200_OK)









