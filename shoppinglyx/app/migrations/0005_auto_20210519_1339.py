# Generated by Django 3.1.3 on 2021-05-19 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210517_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Packed', 'Packed'), ('Delivered', 'Delivered'), ('On the way', 'On the way'), ('Accepted', 'Accepted'), ('Cancel', 'Cancel')], default='Pending', max_length=50),
        ),
    ]
