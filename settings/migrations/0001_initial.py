# Generated by Django 2.1.3 on 2019-03-20 21:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehicles', '0003_auto_20190221_2240'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle_Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(help_text='Info', max_length=200)),
                ('size_font', models.CharField(help_text='Vorne', max_length=200)),
                ('size_rear', models.CharField(help_text='Hinten', max_length=200)),
                ('booked', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('login', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vehicles.Vehicle_Type')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='vehicle_setting',
            unique_together={('login', 'type')},
        ),
    ]