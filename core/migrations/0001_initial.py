# Generated by Django 4.2.7 on 2023-11-21 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerOtp',
            fields=[
                ('otp_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(blank=True, max_length=45, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('otp_time', models.DateTimeField(auto_now_add=True)),
                ('otp', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'customer_otp',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RegistrationModel',
            fields=[
                ('customer_id', models.IntegerField(unique=True)),
                ('customer_name', models.CharField(max_length=250, null=True)),
                ('customer_mobile_no', models.BigIntegerField(primary_key=True, serialize=False)),
                ('customer_email_id', models.CharField(max_length=250, null=True)),
                ('customer_gender', models.CharField(max_length=10, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('active', models.SmallIntegerField(default=1)),
                ('password', models.CharField(blank=True, max_length=250, null=True)),
                ('me', models.CharField(blank=True, max_length=14, null=True)),
            ],
            options={
                'db_table': 'Registration_details',
                'managed': True,
            },
        ),
    ]
