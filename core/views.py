import datetime
import hashlib
import logging
import re
from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection, connections, transaction
from errors import *
from .models import RegistrationModel
from constants import *


logger = logging.getLogger(__name__)
# Create your views here.

def registrationUser(request):

    errorkeys = ['Info','Business_Errors','Warnings','System_Errors']
    errordisplay = [[],[],[],[]]
    ec = []
    ek = []

    logger.info("================= started the register function ====================")
    try:
        if request.method == 'POST':
            customerName = request.POST['customer_name'] if request.POST['customer_name'] else None
            customerMobileno = request.POST['customer_mobile_no'] if request.POST['customer_mobile_no'] else None
            customerEmailid = request.POST['customer_email_id']  if request.POST['customer_email_id'] else None
            customerGender = request.POST['customer_gender']  if request.POST['customer_gender'] else None
            creadtedOn = request.POST['created_on']  if request.POST['created_on'] else None
            updatedOn = request.POST['updated_on'] if request.POST['updated_on'] else None
            createdBy = request.POST['cearted_by'] if request.POST['created_by'] else None
            updatedBy = request.POST['updated_by'] if request.POST['updated_by'] else None
            activeStatus = request.POST['active_status'] if request.POST['active_status'] else None
            password = request.POST['password'] if request.POST['password'] else None

            if(customerMobileno in (None,'') or customerEmailid in (None,'') or customerName in (None,'') or password in (None,'')):
                raise Exception('Some Mandatory fields are Missing')
            
            with transaction.atomic():

                if re.match(r"^[6789]{1}\d{9}$", customerMobileno) and re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$",customerEmailid):
                    logger.info("Phone Number & Email Format is Valid")
                else:
                    raise InvalidMailPhoneException("Invalid Phone or Email Format")
                
                mobile_no = RegistrationModel.objects.filter(customer_mobile_no = customerMobileno).exists()

                if mobile_no:
                    raise CustomerExistsException("User Phone Already Exist")
                
                passwordSha256 = hashlib.sha256(password.encode('UTF-8')).hexdigest()
                current_date = str(datetime.utcnow())
                logger.info("=========== adding to the db processing =================")
                
                request_dict = [{
                'customer_name' : customerName,
                'customer_mobile_no' : customerMobileno,
                'customer_email_id' : customerEmailid,
                'customer_gender' : customerGender,
                'created_on' : current_date,
                'updated_on' : current_date,
                'activeStatus' : activeStatus,
                'password' : passwordSha256
            }]
                
            insert_response = RegistrationModel.objects.create(**request_dict)
            customerId = insert_response.customer_id
            logger.info(f"Candidate Data Inserted. Candidate ID -- {customerId}")
            RegistrationModel.objects.create(createdBy = customerId , updatedBy = customerId)
    
            logger.info(f'the details of dict {request_dict}''')
            logger.info("==================== Registration DETAILS END To the DB ==================================")
        return render(request, 'forms/regd.html',{'all_records':request_dict})
            
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
        ec.append(BE001)
        ec.append(BE001MESSAGE)
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
