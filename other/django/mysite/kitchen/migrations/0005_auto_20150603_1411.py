# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0004_auto_20150603_1010'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='storecategory',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='recipeorder',
            name='status',
            field=models.CharField(default=b'0', max_length=1, choices=[(b'0', b'planned'), (b'1', b'complete'), (b'2', b'canceled')]),
            preserve_default=True,
        ),
    ]
