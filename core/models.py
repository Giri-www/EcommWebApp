from django.db import models

# Create your models here.

class RegistrationModel(models.Model):
    customer_id = models.BigAutoField()
    customer_name = models.CharField(max_length=250 ,null=True)
    customer_mobile_no = models.IntegerField(primary_key=True,max_length=10,null=True)
    customer_email_id = models.CharField(max_length=250, null =True ,blank= False)
    customer_gender = models.CharField(max_length = 10, null=True, blank= False)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
     
    class meta:
        managed = True
        db_table = 'RegdUser'

    
