# Generated by Django 5.0.2 on 2024-05-01 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_alter_otpcode_otp_profileimage'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='otpcode',
            name='otp',
            field=models.CharField(default='84836', max_length=6),
        ),
    ]