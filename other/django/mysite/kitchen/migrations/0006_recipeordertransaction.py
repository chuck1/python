# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0005_auto_20150603_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeOrderTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
                ('ingredient', models.ForeignKey(to='kitchen.Ingredient')),
                ('recipeorder', models.ForeignKey(to='kitchen.RecipeOrder')),
                ('unit', models.ForeignKey(to='kitchen.Unit')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
