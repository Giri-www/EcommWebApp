
from django.urls import path
from core.views import * 
from products.views import *

 
urls=[

#Registration
path('signup/',registrationUser),
path('generateotp/',generateOtp),



#Products-Category
path('addupdatecategory/',addupdate_category),
path('fetchallcategory/',fetchCategoryAllDetails)




]