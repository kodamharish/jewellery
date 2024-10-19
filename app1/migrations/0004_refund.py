# Generated by Django 5.1.1 on 2024-10-19 04:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_alter_member_nominee_dob'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('scheme_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.IntegerField()),
                ('maturity_period', models.DateField()),
                ('total_amount_received', models.IntegerField()),
                ('refund_amount', models.IntegerField()),
                ('refund_by', models.CharField(max_length=100)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.member')),
            ],
        ),
    ]
