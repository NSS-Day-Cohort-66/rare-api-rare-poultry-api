# Generated by Django 4.2.7 on 2023-11-20 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0007_reactions_postreactions'),
    ]

    operations = [
        migrations.AddField(
            model_name='rareusers',
            name='rare_username',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]