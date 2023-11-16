from django.db import models

# Create your models here.

class RegistrationModel(models.Model):
    customer_id = models.BigAutoField(primary_key=True)
    customer_name = models.CharField(max_length=250 ,null=True)
    customer_mobileno = models.IntegerField(max_length=10,null=True)
    customer_emailid = models.CharField(max_length=250, null =True ,blank= False)
    
