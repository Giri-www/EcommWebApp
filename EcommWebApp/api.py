
from django.urls import path
from core.views import *

 
urls=[

#Registration
path('signup/',registrationUser),
path('generateotp/',generateOtp),
path('validateotp/',validateOtp)





]