# Generated by Django 4.2.16 on 2024-10-31 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0019_merge_20241010_2313'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$600000$yorx8eJXMDmEFt51j9KQfY$3yFevZgpfw8Hnyzt82ondbyf09ljUMSOdldwQIb+Rcw=', max_length=128),
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
