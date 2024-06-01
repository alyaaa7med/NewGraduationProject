# Generated by Django 5.0.2 on 2024-06-01 00:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_alter_otpcode_otp'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=15)),
                ('date', models.DateField()),
                ('start_at', models.TimeField()),
                ('type', models.CharField(choices=[('standard', 'Standard'), ('premium', 'Premium')], max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('state', models.CharField(choices=[('free', 'Free'), ('booked', 'Booked')], default='free', max_length=10)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.doctor')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('day', 'date', 'start_at', 'doctor')},
            },
        ),
    ]
