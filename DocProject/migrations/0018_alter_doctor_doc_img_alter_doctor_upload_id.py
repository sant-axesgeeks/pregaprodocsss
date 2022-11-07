# Generated by Django 4.0.5 on 2022-06-30 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DocProject', '0017_alter_doctor_doc_img_alter_doctor_upload_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='doc_img',
            field=models.ImageField(default='profile.png', upload_to='doc_img/'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='upload_id',
            field=models.ImageField(blank=True, default='profile.png', null=True, upload_to='upload_id/'),
        ),
    ]
