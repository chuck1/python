# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climb', '0003_auto_20150611_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wall',
            name='area',
            field=models.ForeignKey(blank=True, to='climb.Area', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wall',
            name='location',
            field=models.ForeignKey(blank=True, to='climb.Location', null=True),
            preserve_default=True,
        ),
    ]
