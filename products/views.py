from django.shortcuts import render
from datetime import datetime, timedelta
import hashlib
import logging
import re,random
from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection, connections, transaction
import requests
from errors import *
from constants import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

from products.models import Category

logger = logging.getLogger(__name__)

# Create your views here.

@api_view(['POST'])
def addupdate_category(request):

    errorkeys = ['Info','Business_Errors','Warnings','System_Errors']
    errordisplay = [[],[],[],[]]
    ec = []
    ek = []
    logger.info("================= started the addupdate category  ====================")

    data = request.data
    logger.info(f"request data = {data}")
    
    #if customer_type ==1:
    category = data['category_name']

    if (category is  None  and category == ''): 
            raise InvalidCateogoryException("Cateogory should not be empty")
    
    if 'category_id' in data:
            logger.info(f"category ID (UPDATE): {data['category_id']}")
            Category.objects.filter(category_id=data['category_id']).update(**data)
            return Response({CODE:SUCCESSCODE})



