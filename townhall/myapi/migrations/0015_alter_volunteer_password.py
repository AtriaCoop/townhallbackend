# Generated by Django 5.1 on 2024-09-30 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0014_alter_volunteer_password_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$gfKTXTuY26i0wkHsfn3hh1$aIhrNpm/+O1+usyLq3abBojxO86LKAFXEKaIVzEPN5g=', max_length=128),
        ),
    ]
