# Generated by Django 5.0.6 on 2025-01-12 02:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0022_community_alter_volunteer_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='community_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapi.community'),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$720000$ocIRDFUfNMXWcQkgL8dQs2$gbNWwaxRhJW1Je+yQxeGLtz+9KJ2N6GaQFpYhAt2XC8=', max_length=128),
        ),
    ]
