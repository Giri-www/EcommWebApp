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


@api_view(['GET'])
def fetchCategoryAllDetails(request):
    errorkeys = ['Info','Business_Errors','Warnings','System_Errors']
    errordisplay = [[],[],[],[]]
    ec = []
    ek = []
    logger.info(" ==================== Category Details Started ==============================")
    try:
            data = request.data
            logger.info(f"Category Details {data}")
            page_size = data['page_size']
            page_index = data['page_index']
            ordering = data['ordering'] if data.get('ordering') else {'order_name':'category_id', 'order_type':"ASC"}
            # search_string = data['search_string'] if data.get('search_string') else None

            search_filter_query=""
            pagination_query=""

            cursor = connection.cursor()

            CATEGORY_ORDERING_MAP = {
                "category_id": "c.category_id",
                "category_name":"c.category_name"

            }
            logger.info(f'''lets see {CATEGORY_ORDERING_MAP}''')

            starting_point = page_index * page_size

            fetc_qry = f'''SELECT c.category_id, c.category_name FROM ecommweb.products_category c '''

            cursor.execute(fetc_qry)
            cols = [col[0] for col in cursor.description]
            res = [dict(zip(cols, row)) for row in cursor.fetchall()]

            if ordering['order_name'] is not None:
                if ordering['order_name'] in CATEGORY_ORDERING_MAP:
                    pagination_query = f""" ORDER BY {CATEGORY_ORDERING_MAP[ordering['order_name']]} {ordering['order_type']} LIMIT {starting_point},{page_size}"""
                else:
                    raise InvalidOrderingIndexException("Ordering column invalid")
            
            fetc_qry+=pagination_query 
            logger.info(f"fetch{fetc_qry}")
            cursor.execute(fetc_qry)
            cols = [col[0] for col in cursor.description]
            query_result = [
            dict(zip(cols, row))
            for row in cursor.fetchall() ]
            return Response({"page_index": page_index, "page_size": page_size,"total_count": len(res),"details_category":query_result})
        
    except InvalidOrderingIndexException as ioe:
        logger.exception(ioe)
        ec.append(BE007)
        ec.append(BE007MESSAGE)
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
        logger.warning("< ================= END - Fetch Cateogory DETAILS ==================== >")
     

      
            



        



