# Generated by Django 5.0.2 on 2024-04-21 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_appointement_patient_appointement_session_length_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointement',
            name='price',
            field=models.DecimalField(decimal_places=10, max_digits=10, null=True),
        ),
    ]
