# Generated by Django 4.0.4 on 2022-06-24 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DocProject', '0002_alter_subscription_patient_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='BabyName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
