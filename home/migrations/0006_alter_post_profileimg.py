# Generated by Django 4.2.4 on 2023-09-24 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_post_profileimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='profileImg',
            field=models.ImageField(default='default.png', upload_to='profile_images/%Y/%m/%d/'),
        ),
    ]
