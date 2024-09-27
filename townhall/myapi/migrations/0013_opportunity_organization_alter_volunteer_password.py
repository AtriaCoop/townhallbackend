# Generated by Django 5.0.6 on 2024-09-25 03:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0012_alter_opportunity_volunteers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='opportunity',
            name='organization',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapi.organization'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$720000$1P7IOgJHK1CEXSeuyPpbCi$VHpqr633klFpieulLbQ+m0KfCCsWECLRNZViQacJKOE=', max_length=128),
        ),
    ]
