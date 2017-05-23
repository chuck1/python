# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0007_transaction_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='price',
        ),
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
