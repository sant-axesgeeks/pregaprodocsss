# Generated by Django 4.0.4 on 2022-06-22 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DocProject', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='patient_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='DocProject.patient'),
        ),
    ]
