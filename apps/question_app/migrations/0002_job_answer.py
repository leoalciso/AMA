# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-11-15 23:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_to_q', to='question_app.Answer'),
        ),
    ]
