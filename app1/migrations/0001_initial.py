# Generated by Django 5.1.1 on 2024-10-23 03:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('pin', models.CharField(max_length=15, null=True)),
                ('phone_number', models.IntegerField(null=True)),
                ('aadhaar', models.CharField(max_length=50, null=True)),
                ('pan', models.CharField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('join_date', models.DateField()),
                ('end_date', models.DateField()),
                ('nominee_name', models.CharField(max_length=50, null=True)),
                ('nominee_email', models.EmailField(max_length=254, null=True)),
                ('nominee_phone_number', models.IntegerField(null=True)),
                ('nominee_dob', models.DateField(null=True)),
                ('nominee_adhaar', models.CharField(max_length=50, null=True)),
                ('nominee_pan', models.CharField(max_length=50, null=True)),
                ('referred_person_name', models.CharField(max_length=50, null=True)),
                ('referred_person_id', models.CharField(max_length=50, null=True)),
                ('referred_person_referral_code', models.CharField(max_length=50, null=True)),
                ('member_referral_code', models.CharField(max_length=8, null=True, unique=True)),
                ('referral_points', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('purity', models.CharField(max_length=50)),
                ('rate_10_grams', models.IntegerField()),
                ('rate_1_gram', models.IntegerField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Scheme',
            fields=[
                ('scheme_id', models.AutoField(primary_key=True, serialize=False)),
                ('scheme_name', models.CharField(max_length=100, unique=True)),
                ('scheme_maturity_period', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36')], max_length=50)),
                ('scheme_benefit', models.CharField(choices=[('No wastage - No Making charges', 'No wastage - No Making charges')], max_length=50)),
                ('scheme_installment_amount', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.IntegerField()),
            ],
        ),
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
        migrations.AddField(
            model_name='member',
            name='scheme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.scheme'),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('voucher_no', models.IntegerField(blank=True, null=True, unique=True)),
                ('transaction', models.CharField(max_length=50)),
                ('receipt_date', models.DateField()),
                ('receipt_time', models.TimeField(auto_now=True)),
                ('receipt_amount', models.IntegerField()),
                ('scheme_name', models.CharField(max_length=50)),
                ('payment_mode', models.CharField(max_length=50)),
                ('remarks', models.CharField(max_length=50)),
                ('ent_by', models.CharField(max_length=50)),
                ('installment_in_grams', models.DecimalField(decimal_places=3, max_digits=10)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.member')),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.user'),
        ),
    ]
