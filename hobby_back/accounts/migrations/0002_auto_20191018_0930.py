# Generated by Django 2.2.6 on 2019-10-18 09:30

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userLike',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default='', max_length=50), blank=True, default=list, null=True, size=8), null=True, size=2),
        ),
    ]