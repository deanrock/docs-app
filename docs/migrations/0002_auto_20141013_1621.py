# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='url',
            field=models.CharField(max_length=255, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='url',
            field=models.CharField(max_length=255, default=''),
            preserve_default=False,
        ),
    ]
