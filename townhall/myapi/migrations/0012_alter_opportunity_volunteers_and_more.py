# Generated by Django 5.0.6 on 2024-09-19 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0011_remove_post_user_post_volunteer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opportunity',
            name='volunteers',
            field=models.ManyToManyField(blank=True, related_name='opportunities', to='myapi.volunteer'),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$720000$ktuPsf2eYWdpysUBRTVnhe$haenxePJa6soDIK8MCafL12CbSU5JrIhsD7DFOPQe98=', max_length=128),
        ),
    ]
