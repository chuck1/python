# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0006_recipeordertransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='price',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
