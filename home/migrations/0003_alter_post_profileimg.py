# Generated by Django 4.2.4 on 2023-09-24 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_post_bio_post_location_post_profileimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='profileImg',
            field=models.ImageField(upload_to='profile_images/'),
        ),
    ]
