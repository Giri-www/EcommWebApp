from datetime import datetime
import hashlib
import logging
import re
from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection, connections, transaction
from errors import *
from .models import RegistrationModel
from constants import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger(__name__)

# Create your views here.
@api_view(['POST'])
def registrationUser(request):
    

    errorkeys = ['Info','Business_Errors','Warnings','System_Errors']
    errordisplay = [[],[],[],[]]
    ec = []
    ek = []

    logger.info("================= started the register function ====================")
    try:
            data = request.data
            logger.info(f"Requested Data = {data}")
            customerName = data['customer_name'] 
            customerMobileno = data['customer_mobile_no'] 
            customerEmailid = data['customer_email_id'] 
            customerGender = data['customer_gender']  if data.get('customer_gender') else None
            creadtedOn = data['created_on']  if data.get('created_on') else None
            updatedOn = data['updated_on'] if data.get('updated_on') else None
            createdBy = data['cearted_by'] if data.get('created_by') else None
            updatedBy = data['updated_by'] if data.get('updated_by') else None
            activeStatus = data['active_status'] if data.get('active_status') else None
            password = data['password'] 

            if(customerMobileno in (None,'') or customerEmailid in (None,'') or customerName in (None,'') or password in (None,'')):
                raise MandatoryInputMissingException('Some Mandatory fields are Missing')
            
            with transaction.atomic():

                if re.match(r"^[6789]{1}\d{9}$",str(customerMobileno)) and re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$",str(customerEmailid)):
                    logger.info("Phone Number & Email Format is Valid")
                
                    mobile_no = RegistrationModel.objects.filter(customer_mobile_no = customerMobileno).exists()

                    if mobile_no:
                        raise CustomerExistsException("User Phone Already Exist")
                else:
                    raise InvalidMailPhoneException("Invalid Phone or Email Format")
                passwordSha256 = hashlib.sha256(password.encode('UTF-8')).hexdigest()
                current_date = str(datetime.utcnow())
                logger.info("=========== adding to the db processing =================")
                customerMobileno1 = int(customerMobileno)
                
                request_dict = {
                'customer_name' : customerName,
                'customer_mobile_no' : customerMobileno1,
                'customer_email_id' : customerEmailid,
                'customer_gender' : customerGender,
                'created_on' : current_date,
                'updated_on' : current_date,
                'active' : activeStatus,
                'password' : passwordSha256
            }
           
            RegistrationModel.objects.create(**request_dict)
            # customerId = RegistrationModel.customer_id
            # logger.info(f"Candidate Data Inserted. Candidate ID -- {customerId}")
            # RegistrationModel.objects.create(createdBy = customerId , updatedBy = customerId)
    
            logger.info(f'the details of dict {request_dict}''')
            logger.info("==================== Registration DETAILS END To the DB ==================================")
            return Response({CODE: SUCCESSCODE})
            
    except MandatoryInputMissingException as mime:
        logger.exception(mime)
        ec.append(BE001)
        ec.append(BE001MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[1].append(dict(zip(ek,ec)))
        return JsonResponse ({"Errors":dict(zip(errorkeys,errordisplay))})
    
    except CustomerExistsException as cee:
        logger.exception(cee)
        ec.append(BE005)
        ec.append(BE005MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[1].append(dict(zip(ek,ec)))
        return JsonResponse ({"Errors":dict(zip(errorkeys,errordisplay))})
    
    except InvalidMailPhoneException as ipee:
        logger.exception(ipee)
        ec.append(BE003)
        ec.append(BE003MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[1].append(dict(zip(ek,ec)))
        return JsonResponse ({"Errors":dict(zip(errorkeys,errordisplay))})
       
    except Exception as e:
        logger.exception(e)
        ec.append(SE001)
        ec.append(SE001MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[3].append(dict(zip(ek,ec)))
        return JsonResponse ({"Errors":dict(zip(errorkeys,errordisplay))})
    
    finally:
        connections.close_all()
        logger.info("Database connection is closed")
        logger.info("<=============== End - Candidate Registration ===============>")
