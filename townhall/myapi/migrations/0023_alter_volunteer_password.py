# Generated by Django 5.1.5 on 2025-02-06 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0022_alter_volunteer_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$TCicmMGBnx7NzaYok32AGl$Krw3GhLfbDpBeKDMxMBmttsD/fsUKRD25ktBDNovfs8=', max_length=128),
        ),
    ]
