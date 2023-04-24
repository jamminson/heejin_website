# Generated by Django 3.2.5 on 2023-04-20 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20230420_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='num_distributed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='num_produced',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='catalog.product'),
        ),
    ]
