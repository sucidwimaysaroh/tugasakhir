# Generated by Django 4.0.5 on 2022-06-19 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classify', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='classify',
            name='fitur',
            field=models.TextField(default=123),
            preserve_default=False,
        ),
    ]
