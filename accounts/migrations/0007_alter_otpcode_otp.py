# Generated by Django 5.0.2 on 2024-03-21 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_otpcode_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='otp',
            field=models.CharField(default='1411b', max_length=6),
        ),
    ]
