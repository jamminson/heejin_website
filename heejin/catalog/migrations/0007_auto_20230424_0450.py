# Generated by Django 3.2.5 on 2023-04-23 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_order_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='num_distributed',
            new_name='vol',
        ),
        migrations.RemoveField(
            model_name='order',
            name='num_produced',
        ),
    ]
