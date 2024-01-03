from django.shortcuts import render

# Create your views here.

# views.py
from rest_framework import generics
from .models import Order
from .serializers import *

class OrderListAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
