# Generated by Django 3.1.3 on 2021-05-30 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210519_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('On the way', 'On the way'), ('Packed', 'Packed'), ('Delivered', 'Delivered'), ('Accepted', 'Accepted'), ('Cancel', 'Cancel')], default='Pending', max_length=50),
        ),
    ]
