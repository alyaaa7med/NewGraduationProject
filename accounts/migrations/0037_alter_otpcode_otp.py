# Generated by Django 5.0.2 on 2024-05-21 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0036_alter_otpcode_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='otp',
            field=models.CharField(default='0410e', max_length=6),
        ),
    ]