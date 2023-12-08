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

    try:
        data = request.data
        logger.info(f"request data = {data}")
        
        #if customer_type ==1:
        category = data['category_name']
        #     data['delete_flag'] =  1

        if (category is  None  and category == ''): 
                raise InvalidCateogoryException("Cateogory should not be empty")
        
        if 'category_id' in data:
                logger.info(f"category ID (UPDATE): {data['category_id']}")
                Category.objects.filter(category_id=data['category_id']).update(**data)
                return Response({CODE:SUCCESSCODE})
        else:
                Category.objects.create(**data)
                return Response({CODE:SUCCESSCODE})
    except InvalidCateogoryException as ice:
        logger.exception(ice)
        ec.append(BE006)
        ec.append(BE006MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[1].append(dict(zip(ek,ec)))
        return Response ({ERROR:dict(zip(errorkeys,errordisplay))})
    
    except Exception as e:
        logger.exception(e)
        ec.append(SE001)
        ec.append(SE001MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[3].append(dict(zip(ek,ec)))
        return Response ({ERROR:dict(zip(errorkeys,errordisplay))})
    finally:
        logger.warning("< ================= END - ADD Cateogory DETAILS ==================== >")
            



        


