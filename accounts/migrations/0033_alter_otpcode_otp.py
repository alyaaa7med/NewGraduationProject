# Generated by Django 5.0.2 on 2024-05-15 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0032_alter_otpcode_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='otp',
            field=models.CharField(default='591c3', max_length=6),
        ),
    ]
