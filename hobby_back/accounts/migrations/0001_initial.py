# Generated by Django 2.2.6 on 2019-10-21 10:38

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=100)),
                ('userNickName', models.CharField(max_length=100)),
                ('userSex', models.CharField(max_length=20)),
                ('userAge', models.IntegerField()),
                ('userImage', models.ImageField(blank=True, upload_to='')),
                ('userGrade', models.IntegerField(default=1)),
                ('userAddress', models.CharField(blank=True, max_length=200)),
                ('userLike', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default='', max_length=50), blank=True, default=list, null=True, size=8), null=True, size=2)),
            ],
        ),
        migrations.CreateModel(
            name='PostOnetone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.TextField()),
                ('answer', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.User')),
            ],
        ),
        migrations.CreateModel(
            name='payInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payNum', models.CharField(max_length=100)),
                ('payAmount', models.IntegerField()),
                ('payDate', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.User')),
            ],
        ),
    ]
