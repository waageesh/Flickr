# Generated by Django 3.0.5 on 2020-05-07 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('group_id', models.IntegerField()),
                ('group_name', models.CharField(max_length=50)),
                ('image_id', models.IntegerField()),
                ('user', models.CharField(max_length=50)),
            ],
        ),
    ]
