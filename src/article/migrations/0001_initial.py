# Generated by Django 3.0.3 on 2020-04-06 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(max_length=120)),
                ('body', models.CharField(max_length=5000)),
                ('url', models.TextField()),
                ('image', models.ImageField(upload_to='')),
                ('category', models.CharField(max_length=100)),
                ('favourite', models.BooleanField(default=False)),
                ('date', models.DateTimeField()),
            ],
        ),
    ]