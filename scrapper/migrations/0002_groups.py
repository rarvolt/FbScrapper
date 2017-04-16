# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-16 11:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterModelOptions(
            name='place',
            options={},
        ),
        migrations.AddField(
            model_name='group',
            name='places',
            field=models.ManyToManyField(blank=True, related_name='groups', to='scrapper.Place'),
        ),
    ]