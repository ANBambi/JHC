# Generated by Django 4.2.5 on 2023-10-04 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrot_app', '0004_image_remove_post_images_post_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthdate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default='example@oruemi.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='profile_pictures/default_profile_picture.png', upload_to='profile_pictures/'),
        ),
    ]