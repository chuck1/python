# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0002_remove_item_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='category2',
            new_name='category',
        ),
    ]
