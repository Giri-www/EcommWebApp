from datetime import datetime, timedelta
import hashlib
import logging
import re,random
from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection, connections, transaction
import requests
from errors import *
from .models import RegistrationModel,CustomerOtp
from constants import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

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
                    email_id = RegistrationModel.objects.filter(email_id = customerEmailid).exists()

                    if mobile_no:
                        raise CustomerExistsException("User Phone Already Exist")
                    elif email_id:
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




@api_view(['POST'])
def generateOtp(requests):
    try:
        print("try")
        logger.info("api  i")
        result = generateotp_rest(requests)  
        logger.info(f'result is {result}''') 
        print("ok")
        return Response({CODE:SUCCESSCODE})
    except InvalidMailPhoneException as e:
        print(f"Error: {e}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error: {e}")
        return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def generateotp_rest(requests):
    logger.info("=============== Generate Otp started ================")
    errorkeys = ['Info','Business_Errors','Warnings','System_Errors']
    errordisplay = [[],[],[],[]]
    ec = []
    ek = []
    try:
            data = requests.data
            logger.info(f"Request Data : {data}")
            phone = data['phone']
            email = data['email']
            otp_flag = data['otp_flag'] if data.get('otp_flag') else None
            #for registration  
            if otp_flag == 1:   
                if phone and email is not None:
                    logger.info("Customer phone is not None")
                    if re.match(r"^[6789]{1}\d{9}$", str(phone)) and re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$",str(email)):
                            logger.info('Customer User Name is Phone') 
                            verification_code_validity = 480 
                            otp =  random.randrange(100000, 999999)
                            otp = str(otp)
                            logger.info(f'otp is {otp}')
                            otptime = str(datetime.utcnow())
                            otpdata = {"otp":str(otp),"phone":phone,"email":email,"otp_time":otptime,"expire_time": (timedelta(minutes=verification_code_validity) + datetime.utcnow()).strftime("%Y-%m-%d %H:%M:%S")}
                            logger.info(f'otpdata is {otpdata}')
                            otp_dict = CustomerOtp.objects.create(**otpdata)
                            logger.info("<================ End - Customer Generate OTP ===============>")
                            return otp
                    else:
                        raise InvalidMailPhoneException("Email OR phone no is not valid")      
                else:
                    raise InvalidMailPhoneException("Email OR Phone no should not be null")
            #for LogIn    
            if otp_flag == 2:   
                if phone and email is not None:
                    logger.info("Customer phone is not None")
                    if re.match(r"^[6789]{1}\d{9}$", str(phone)) and re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$",str(email)):
                            logger.info('Customer User Name is Phone')  
                            otp =  random.randrange(100000, 999999)
                            verification_code_validity = 480
                            otp = str(otp)
                            logger.info(f'otp is {otp}')
                            otptime = str(datetime.utcnow())
                            otpdata = {"otp":str(otp),"phone":phone,"email":email,"otp_time":otptime,"expire_time": (timedelta(minutes=verification_code_validity) + datetime.utcnow()).strftime("%Y-%m-%d %H:%M:%S")}
                            logger.info(f'otpdata is {otpdata}')
                            otp_dict = CustomerOtp.objects.create(**otpdata)
                            logger.info("<================ End - Customer Generate OTP ===============>")
                            return otpdata
                    else:
                        raise InvalidMailPhoneException("Email OR phone no is not valid")      
                else:
                    raise InvalidMailPhoneException("Email OR Phone no should not be null")
                
    except InvalidMailPhoneException as ipee:
        logger.exception(ipee)
        ec.append(BE003)
        ec.append(BE003MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        errordisplay[1].append(dict(zip(ek,ec)))
        response = {"Errors":dict(zip(errorkeys,errordisplay))}
        return Response(response)
    
    except Exception as e:
        logger.exception(e)
        ec.append(SE001)
        ec.append(SE001MESSAGE)
        ek.append(CODE)
        ek.append(MESSAGE)
        response = errordisplay[3].append(dict(zip(ek,ec)))
        return Response(response)
    
    finally:
        connections.close_all()
        logger.info("<================ End finaly connrctions - Customer Generate OTP ===============>")




def validateOtp(email,code):

    logger.info("<======================== Start - Validate OTP ========================>")
    try:
        # cursor = connection.cursor()
        logger.info("====== try Block =====")
        otp_result = CustomerOtp.objects.filter(Q(email=email) & Q(otp=code)).values('otp_id','email', 'otp_time', 'otp', 'expire_time').order_by('-otp_id')[:1]
        
        if len(otp_result) > 0:
            otp_result = otp_result[0]
            otp = otp_result['otp']
            customer_otp = otp_result['otp_id']

            current_time = datetime.strptime(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            expiry_time =  datetime.strptime(otp_result['expire_time'].strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
    
            if current_time > expiry_time: 
                status = 1
                update_data = {'otp': 'expired'}
                if otp != 'used':
                    CustomerOtp.objects.filter(Q(email=email) & Q(otp=code)).update(**update_data)
            else:
                if str(otp) == str(code):
                    logger.info('Customer OTP matches correctly')
                    # query = f'''UPDATE customer_otp SET otp = 'used' WHERE otp_id = {customer_otp}'''
                    update_data = {'otp': 'used'}
                    CustomerOtp.objects.filter(Q(email=email) & Q(otp=code)).update(**update_data)
                    logger.info("Successfully verify email")
                    status = 2
                else:
                    status = 3
                    logger.info("Wrong Verification Code")
        else:
            status = 4
            logger.info("Wrong email or verification code")

    except Exception as e:
        logger.exception(e)
        status = 5
        
    finally:
        logger.info("================ Sucessfully End Validate Otp finally Block ==================")
        return status