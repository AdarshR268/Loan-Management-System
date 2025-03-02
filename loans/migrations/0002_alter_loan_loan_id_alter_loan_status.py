# Generated by Django 5.1.6 on 2025-03-01 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='loan_id',
            field=models.CharField(db_index=True, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('CLOSED', 'Closed'), ('FORECLOSED', 'Foreclosed')], db_index=True, default='ACTIVE', max_length=10),
        ),
    ]
