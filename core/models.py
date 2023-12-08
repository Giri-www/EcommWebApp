from django.db import models

# Create your models here.

class RegistrationModel(models.Model):
    customer_id = models.IntegerField(unique=True, auto_created=True)
    customer_name = models.CharField(max_length=250 ,null=True)
    customer_mobile_no = models.BigIntegerField(primary_key=True)
    customer_email_id = models.CharField(max_length=250, null =True ,blank= False)
    customer_gender = models.CharField(max_length = 10, null=True, blank= False)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    active = models.SmallIntegerField(default=1)
    password = models.CharField(max_length=250, null=True, blank=True)
    customer_type = models.IntegerField(max_length=14, null=True, blank=True)
     
    class Meta:
        managed = True
        db_table = 'Registration_details'


class CustomerOtp(models.Model):
    otp_id = models.BigAutoField(primary_key=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    otp_time = models.DateTimeField(auto_now_add=True)
    otp = models.CharField(max_length=45, blank=True, null=True)
    expire_time = models.DateTimeField(blank=True, null=True)
    # otp1 = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'customer_otp'

    
