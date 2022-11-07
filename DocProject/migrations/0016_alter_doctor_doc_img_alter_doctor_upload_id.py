# Generated by Django 4.0.5 on 2022-06-30 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DocProject', '0015_alter_doctor_doc_img_alter_doctor_upload_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='doc_img',
            field=models.ImageField(default='static/profile.png', upload_to='doc_img/'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='upload_id',
            field=models.ImageField(blank=True, default='static/profile.png', null=True, upload_to='upload_id/'),
        ),
    ]
