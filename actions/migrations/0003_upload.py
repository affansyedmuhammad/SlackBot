# Generated by Django 4.0.4 on 2022-06-05 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0002_messageinformation_channel'),
    ]

    operations = [
        migrations.CreateModel(
            name='upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('upload', models.FileField(upload_to='Files')),
            ],
        ),
    ]
