
from django.urls import path
from core.views import * 
from products.views import *
# api.py
from Order.views import OrderListAPIView, OrderDetailAPIView


 
urls=[

#Registration
path('signup/',registrationUser),
path('generateotp/',generateOtp),



#Products-Category
path('addupdatecategory/',addupdate_category),
path('fetchallcategory/',fetchCategoryAllDetails),


#
path('orders/',OrderListAPIView.as_view(), name='order-list'),
path('orderdetail/',OrderDetailAPIView.as_view(), name='order-detail'),

]