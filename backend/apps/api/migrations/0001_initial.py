# Generated by Django 4.1.2 on 2022-12-10 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SecureDropUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=180)),
                ('email', models.CharField(max_length=180)),
                ('passwd', models.CharField(max_length=180)),
                ('pubkey', models.CharField(max_length=360)),
            ],
        ),
    ]
