# Generated by Django 4.2.7 on 2023-11-21 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_registrationmodel_me_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerotp',
            name='expire_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]