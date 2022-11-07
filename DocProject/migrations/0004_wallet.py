# Generated by Django 4.0.4 on 2022-06-27 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DocProject', '0003_babyname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(blank=True, max_length=200, null=True)),
                ('total_amount', models.FloatField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DocProject.patient')),
            ],
        ),
    ]
