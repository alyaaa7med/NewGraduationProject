# Generated by Django 5.0.2 on 2024-04-06 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_otpcode_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='otp',
            field=models.CharField(default='0b3fb', max_length=6),
        ),
    ]