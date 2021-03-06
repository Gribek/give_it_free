# Generated by Django 2.1.5 on 2019-01-23 12:37

import GiveItFreeApp.models
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gift_type', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=32), size=None)),
                ('number_of_bags', models.SmallIntegerField()),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('transfer_date', models.DateField(null=True)),
                ('is_transferred', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PickUpAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=32)),
                ('postal_code', models.CharField(max_length=8)),
                ('phone_number', models.CharField(max_length=16)),
                ('pick_up_date', models.DateField()),
                ('pick_up_time', models.TimeField()),
                ('comments', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrustedInstitution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('purpose', models.CharField(max_length=128)),
                ('localization', models.CharField(max_length=64)),
                ('target_groups', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=32), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', GiveItFreeApp.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='gift',
            name='giver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='gift',
            name='pick_up_address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='GiveItFreeApp.PickUpAddress'),
        ),
        migrations.AddField(
            model_name='gift',
            name='trusted_institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GiveItFreeApp.TrustedInstitution'),
        ),
    ]
