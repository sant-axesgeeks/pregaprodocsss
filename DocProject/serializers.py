from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
from .models import *
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'password','password2']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

  # def create(self, validate_data):
  #   return User.objects.create_user(**validate_data)

class DoctorRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = Doctor
    fields='__all__'
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

  # def create(self, validate_data):
  #   return Doctor.objects.create(**validate_data)

# class PatientRegistrationSerializer(serializers.ModelSerializer):
#   # We are writing this becoz we need confirm password field in our Registratin Request
#   password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
#   class Meta:
#     model = Patient
#     fields=['email', 'name', 'phone_number','password', 'password2', 'tc']
#     extra_kwargs={
#       'password':{'write_only':True}
#     }

#   # Validating Password and Confirm Password while Registration
#   def validate(self, attrs):
#     password = attrs.get('password')
#     password2 = attrs.get('password2')
#     if password != password2:
#       raise serializers.ValidationError("Password and Confirm Password doesn't match")
#     return attrs

#   def create(self, validate_data):
#     return Patient.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class PatientProfileSerializer(serializers.ModelSerializer):
  email = ReadOnlyField(source='user.email')
  class Meta:
    model = Patient
    fields =['email' ,'name', 'age','phone_number','video_url','package','tc']

class appointmentSerializer(serializers.ModelSerializer):
  appointment_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')
  class Meta:
    model = Appointment
    fields = ['appointment_date']

class getappointmentSerializer(serializers.ModelSerializer):
  appointment_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')
  class Meta:
    model = Appointment
    fields = ['__all__']

class DoctorProfileSerializer(serializers.ModelSerializer):
  email = ReadOnlyField(source='user.email')
  class Meta:
    model = Doctor
    fields =['name','phone_number','tc']
    
class medicalcouncilSerializer(serializers.ModelSerializer):
  class Meta:
    model = MedicalCouncil
    fields = ['state1','state2','state3','state4','state5','state6','state7','state8','state9','state10','state11','state12','state13','state14','state15','state16','state17','state18','state19','state20','state21','state22','state23','state24','state25','state26','state27','state28','state29','state30',]
    
class Login_Serializer(serializers.ModelSerializer):
  class Meta:
    model = Doctor
    fields = ['phone_number']

class Verify_Serializer(serializers.ModelSerializer):
  class Meta:
    model = Doctor
    fields = ['otp']