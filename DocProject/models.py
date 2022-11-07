from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.conf import settings

class UserManager(BaseUserManager):
  def create_user(self, email,password=None,password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
         
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email,password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
      
      )
      user.is_admin = True
      user.save(using=self._db)
      return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email',max_length=255,unique=True,)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Doctor(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=200,null=True,blank=True)
  profession = models.CharField(max_length=200,null=True,blank=True)
  qualification = models.CharField(max_length=200,null=True,blank=True)
  otp = models.CharField(max_length=100,null=True,blank=True)
  upload_id = models.ImageField(upload_to='upload_id/',null=True,blank=True)
  working_location1 = models.CharField(max_length=200,null=True,blank=True)
  # working_location1_img = models.ImageField(upload_to='working_location1_img/',default = 'profile.png',null=True,blank=True)
  working_location2 = models.CharField(max_length=200,null=True,blank=True)
  working_location2_img = models.ImageField(upload_to='working_location2_img/',null=True,blank=True)
  working_location3 = models.CharField(max_length=200,null=True,blank=True)
  working_location3_img = models.ImageField(upload_to='working_location3_img/',null=True,blank=True)
  working_location4 = models.CharField(max_length=200,null=True,blank=True)
  working_location4_img = models.ImageField(upload_to='working_location4_img/',null=True,blank=True)
  working_location5 = models.CharField(max_length=200,null=True,blank=True)
  working_location5_img = models.ImageField(upload_to='working_location5_img/',null=True,blank=True)
  experience = models.CharField(max_length=200,null=True,blank=True)
  longitude_1 = models.FloatField(null=True,blank=True)
  latitude_1 = models.FloatField(null=True,blank=True)
  doc_img = models.ImageField(upload_to = 'doc_img/',null = True, blank=True)
  phone_number = models.CharField(max_length=20,blank=True,null=True)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)


class Patient(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  con_or_preg_type = models.CharField(max_length=200,null=True,blank=True)
  age = models.IntegerField(null=True,blank=True)
  otp = models.CharField(max_length=100,null=True,blank=True)
  name = models.CharField(max_length=200,null=True,blank=True)
  phone_number = models.CharField(max_length=20, blank=True)
  video_url = models.CharField(max_length=200,default="http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4")
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class subscription(models.Model):
  patient_id = models.ForeignKey(Patient, null=True,blank = True,on_delete=models.CASCADE)
  package = models.CharField(max_length=200,null=True,blank=True)
  razorpay_payment_id = models.CharField(max_length=200,null=True,blank=True)
  amount = models.CharField(max_length=200,null=True,blank=True)

class Appointment(models.Model):
  patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
  doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
  appointment_date = models.DateField(null=True,blank=True)
  appointment_time = models.CharField(max_length=500,null=True,blank=True)
  appointment_url = models.CharField(max_length=500,null=True,blank=True)
  ispatientcompleted = models.BooleanField(default=False)
  url_password = models.CharField(max_length=500,null=True,blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


class DocAppointment(models.Model):
  patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
  doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
  appointment_date = models.DateField(null=True,blank=True)
  appointment_time = models.CharField(max_length=500,null=True,blank=True)
  appointment_url = models.CharField(max_length=500,null=True,blank=True)
  isdoctorcompleted = models.BooleanField(default=False)
  url_password = models.CharField(max_length=500,null=True,blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
class CompletedAppointment(models.Model):
  patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
  doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
  appointment_date = models.DateField(null=True,blank=True)
  appointment_time = models.CharField(max_length=500,null=True,blank=True)
  appointment_url = models.CharField(max_length=500,null=True,blank=True)
  
  
class MedicalCouncil(models.Model):
  state1 = models.CharField(max_length=200,null=True,blank=True)
  state2 = models.CharField(max_length=200,null=True,blank=True)
  state3 = models.CharField(max_length=200,null=True,blank=True)
  state4 = models.CharField(max_length=200,null=True,blank=True)
  state5 = models.CharField(max_length=200,null=True,blank=True)
  state6 = models.CharField(max_length=200,null=True,blank=True)
  state7 = models.CharField(max_length=200,null=True,blank=True)
  state8 = models.CharField(max_length=200,null=True,blank=True)
  state9 = models.CharField(max_length=200,null=True,blank=True)
  state10 = models.CharField(max_length=200,null=True,blank=True)
  state11 = models.CharField(max_length=200,null=True,blank=True)
  state12 = models.CharField(max_length=200,null=True,blank=True)
  state13 = models.CharField(max_length=200,null=True,blank=True)
  state14 = models.CharField(max_length=200,null=True,blank=True)
  state15 = models.CharField(max_length=200,null=True,blank=True)
  state16 = models.CharField(max_length=200,null=True,blank=True)
  state17 = models.CharField(max_length=200,null=True,blank=True)
  state18 = models.CharField(max_length=200,null=True,blank=True)
  state19 = models.CharField(max_length=200,null=True,blank=True)
  state20 = models.CharField(max_length=200,null=True,blank=True)
  state21 = models.CharField(max_length=200,null=True,blank=True)
  state22 = models.CharField(max_length=200,null=True,blank=True)
  state23 = models.CharField(max_length=200,null=True,blank=True)
  state24 = models.CharField(max_length=200,null=True,blank=True)
  state25 = models.CharField(max_length=200,null=True,blank=True)
  state26 = models.CharField(max_length=200,null=True,blank=True)
  state27 = models.CharField(max_length=200,null=True,blank=True)
  state28 = models.CharField(max_length=200,null=True,blank=True)
  state29 = models.CharField(max_length=200,null=True,blank=True)
  state30 = models.CharField(max_length=200,null=True,blank=True)

class AskQuery(models.Model):
  patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
  doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
  query = models.CharField(max_length=500,null=True,blank=True)
  answer = models.CharField(max_length=500,null=True,blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class BabyName(models.Model):
  name = models.CharField(max_length=200,null=True,blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Wallet(models.Model):
  doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
  amount = models.FloatField(max_length=200,null=True,blank=True)
  total_amount = models.FloatField(max_length=200,null=True,blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
  doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
  amount = models.FloatField(max_length=200,null=True,blank=True)
  description = models.CharField(max_length=500,null=True,blank=True)
  transaction_id = models.CharField(max_length=500,null=True,blank=True)
  transaction_type = models.CharField(max_length=500,null=True,blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now=True)

class Blog(models.Model):
  doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
  title = models.CharField(max_length=500,null=True,blank=True)
  content = models.CharField(max_length=500,null=True,blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
class Patient_Location(models.Model):
  patient=models.ForeignKey(Patient, on_delete=models.CASCADE)
  longitude_2 = models.FloatField(max_length=200,null=True,blank=True)
  latitude_2 = models.FloatField(max_length=200,null=True,blank=True)