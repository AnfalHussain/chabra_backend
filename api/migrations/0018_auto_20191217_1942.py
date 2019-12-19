# Generated by Django 2.2.6 on 2019-12-17 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20191215_2129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Origin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('Fruit', 'Fruit'), ('Vegetable', 'Vegetable')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='origin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='api.Origin'),
        ),
    ]
