# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lit', '0002_publication_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='code',
            field=models.CharField(default=b'', max_length=128),
            preserve_default=True,
        ),
    ]
