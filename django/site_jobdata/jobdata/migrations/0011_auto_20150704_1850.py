# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobdata', '0010_auto_20150704_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='template',
            field=models.ForeignKey(blank=True, to='jobdata.DocTemplate', null=True),
            preserve_default=True,
        ),
    ]
