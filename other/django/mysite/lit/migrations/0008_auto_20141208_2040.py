# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lit', '0007_auto_20141208_2038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publication',
            old_name='type',
            new_name='_type',
        ),
    ]
