# Generated by Django 4.2.7 on 2023-12-07 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_customerotp_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationmodel',
            name='customer_id',
            field=models.IntegerField(auto_created=True, unique=True),
        ),
    ]