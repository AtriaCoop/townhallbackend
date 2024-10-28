# Generated by Django 5.0.4 on 2024-10-27 23:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0019_merge_20241010_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$720000$CgAv3G0QoRA7ZPB3g1clAf$VKDdeCQoTRm8cQVN78xEhEwtItRZN6UCwcgsmQQImO0=', max_length=128),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('location', models.CharField(max_length=100)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapi.organization')),
            ],
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
