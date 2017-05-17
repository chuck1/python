# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lit', '0003_auto_20141201_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='code',
            field=models.CharField(default=b'', max_length=128, null=True),
            preserve_default=True,
        ),
    ]
