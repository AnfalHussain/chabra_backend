# Generated by Django 2.2.6 on 2019-10-21 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='origin',
            field=models.CharField(default='Kuwait', max_length=50),
            preserve_default=False,
        ),
    ]