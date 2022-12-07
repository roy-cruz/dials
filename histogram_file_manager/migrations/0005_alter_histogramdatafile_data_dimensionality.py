# Generated by Django 4.1.3 on 2022-12-07 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('histogram_file_manager', '0004_alter_histogramdatafile_data_dimensionality_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='histogramdatafile',
            name='data_dimensionality',
            field=models.PositiveIntegerField(blank=True, choices=[(0, 'Unknown'), (1, '1D'), (2, '2D'), (3, '1D+2D')], default=0),
        ),
    ]
