# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lit', '0006_auto_20141208_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='type',
            field=models.ForeignKey(default=None, to='lit.Type'),
            preserve_default=False,
        ),
    ]
