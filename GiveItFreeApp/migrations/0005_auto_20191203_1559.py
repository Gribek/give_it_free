# Generated by Django 2.2.7 on 2019-12-03 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GiveItFreeApp', '0004_charitycollection_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charitycollection',
            name='deadline',
            field=models.DateField(verbose_name='Termin końcowy zbiórki'),
        ),
        migrations.AlterField(
            model_name='charitycollection',
            name='items_needed',
            field=models.CharField(max_length=256, verbose_name='Co jest potrzebne'),
        ),
        migrations.AlterField(
            model_name='charitycollection',
            name='purpose',
            field=models.CharField(max_length=256, verbose_name='Cel zbiórki'),
        ),
    ]