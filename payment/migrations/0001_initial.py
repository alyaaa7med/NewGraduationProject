# Generated by Django 5.0.2 on 2024-03-22 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=15)),
                ('date', models.DateField()),
                ('start_at', models.TimeField()),
                ('end_at', models.TimeField()),
                ('type', models.CharField(choices=[('standard', 'Standard'), ('premium', 'Premium')], max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('state', models.CharField(choices=[('free', 'Free'), ('booked', 'Booked')], default='free', max_length=10)),
            ],
        ),
    ]