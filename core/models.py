from django.db import models

# Create your models here.

class RegistrationModel(models.Model):
    customer = models.IntegerField()
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
    me = models.CharField(max_length=14, null=True, blank=True)
     
    class Meta:
        managed = True
        db_table = 'Registration_details'


    
