# Generated by Django 2.1.3 on 2018-12-05 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextM', '0003_auto_20181205_2140'),
    ]

    operations = [
        migrations.CreateModel(
            name='jobinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobname', models.CharField(max_length=200)),
                ('company', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=400)),
                ('location', models.CharField(max_length=200)),
                ('salary', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='DjangoDouble',
        ),
    ]