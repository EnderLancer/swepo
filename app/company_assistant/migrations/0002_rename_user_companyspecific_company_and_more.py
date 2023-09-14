# Generated by Django 4.2.5 on 2023-09-08 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company_assistant', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companyspecific',
            old_name='user',
            new_name='company',
        ),
        migrations.AddField(
            model_name='processcategory',
            name='description',
            field=models.TextField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='processcategory',
            name='name',
            field=models.CharField(default='', max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='creted_companies', to='company_assistant.employer'),
        ),
        migrations.AlterField(
            model_name='company',
            name='description',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='company',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='followed_companies', to='company_assistant.employer'),
        ),
        migrations.AlterField(
            model_name='processcategory',
            name='code',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='specific',
            name='description',
            field=models.TextField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='specific',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='swdprocess',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='processes', to='company_assistant.processcategory'),
        ),
        migrations.AlterField(
            model_name='swdprocess',
            name='description',
            field=models.TextField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='swdprocess',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.CreateModel(
            name='ProcessPractice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, default='', max_length=500)),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practices', to='company_assistant.swdprocess')),
            ],
        ),
    ]
