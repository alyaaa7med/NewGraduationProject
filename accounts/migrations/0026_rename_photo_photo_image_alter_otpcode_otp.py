# Generated by Django 5.0.2 on 2024-04-30 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_photo_alter_otpcode_otp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='photo',
            new_name='image',
        ),
        migrations.AlterField(
            model_name='otpcode',
            name='otp',
            field=models.CharField(default='0c20d', max_length=6),
        ),
    ]
