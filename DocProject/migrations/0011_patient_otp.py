# Generated by Django 4.0.5 on 2022-06-29 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DocProject', '0010_transaction_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='otp',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]