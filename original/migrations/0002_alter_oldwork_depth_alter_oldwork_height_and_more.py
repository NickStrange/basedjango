# Generated by Django 4.0.2 on 2022-02-05 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('original', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oldwork',
            name='depth',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='oldwork',
            name='height',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='oldwork',
            name='width',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
