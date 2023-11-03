# Generated by Django 4.1.5 on 2023-01-10 20:15

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('student', 'student'), ('teacher', 'teacher'), ('doctor', 'doctor')], default='doctor', max_length=11)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], default='male', max_length=6)),
                ('phone', models.CharField(blank=True, max_length=150, null=True, verbose_name='phone')),
                ('emergency_contact_number', models.CharField(blank=True, max_length=150, null=True, verbose_name='Emergency Contact')),
                ('photo', models.ImageField(default='user_default_pic.jpg', upload_to='user_photo', verbose_name='user dp')),
                ('current_address', models.TextField(blank=True, null=True, verbose_name='current address')),
                ('permanent_address', models.TextField(blank=True, null=True, verbose_name='permanent address')),
                ('note', models.TextField(blank=True, null=True, verbose_name='note')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'All User',
                'verbose_name_plural': 'All Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
            ],
            options={
                'verbose_name': 'Doctor',
                'verbose_name_plural': 'Doctors',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.alluser',),
            managers=[
                ('objects', users.models.DoctorManager()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
            ],
            options={
                'verbose_name': 'student',
                'verbose_name_plural': 'students',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.alluser',),
            managers=[
                ('objects', users.models.StudentManager()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.alluser',),
            managers=[
                ('objects', users.models.TeacherManager()),
            ],
        ),
    ]