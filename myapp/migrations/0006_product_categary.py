# Generated by Django 3.0.7 on 2020-06-12 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20200612_0702'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categary',
            field=models.CharField(default='', max_length=50),
        ),
    ]