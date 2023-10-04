# Generated by Django 4.2.5 on 2023-10-04 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BOOK',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FCSKID', models.CharField(blank=True, db_column='FCSKID', default='WsKMWJph', max_length=8, null=True)),
                ('FCCODE', models.CharField(db_column='FCCODE', max_length=30)),
                ('FCNAME', models.CharField(db_column='FCNAME', max_length=30)),
            ],
            options={
                'db_table': 'BOOK',
            },
        ),
        migrations.CreateModel(
            name='COOR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FCSKID', models.CharField(blank=True, db_column='FCSKID', default='YVDsm5uy', max_length=8, null=True)),
                ('FCCODE', models.CharField(db_column='FCCODE', max_length=30)),
                ('FCNAME', models.CharField(db_column='FCNAME', max_length=30)),
            ],
            options={
                'db_table': 'COOR',
            },
        ),
        migrations.CreateModel(
            name='DEPT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FCSKID', models.CharField(blank=True, db_column='FCSKID', default='Scm7r0-S', max_length=8, null=True)),
                ('FCCODE', models.CharField(db_column='FCCODE', max_length=30)),
                ('FCNAME', models.CharField(db_column='FCNAME', max_length=30)),
            ],
            options={
                'db_table': 'DEPT',
            },
        ),
        migrations.CreateModel(
            name='JOB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FCSKID', models.CharField(blank=True, db_column='FCSKID', default='cYACHbB0', max_length=8, null=True)),
                ('FCCODE', models.CharField(db_column='FCCODE', max_length=30)),
                ('FCNAME', models.CharField(db_column='FCNAME', max_length=30)),
            ],
            options={
                'db_table': 'JOB',
            },
        ),
        migrations.CreateModel(
            name='OrderH',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FCDATASER', models.CharField(db_column='FCDATASER', default='$$$9', max_length=4)),
                ('FCSKID', models.CharField(blank=True, db_column='FCSKID', default='4nB0pg4r', max_length=8, null=True)),
                ('FCLUPDAPP', models.CharField(db_column='FCLUPDAPP', max_length=2)),
                ('FCRFTYPE', models.CharField(blank=True, db_column='FCRFTYPE', default='w', max_length=1, null=True)),
                ('FCREFTYPE', models.CharField(db_column='FCREFTYPE', max_length=2)),
                ('FCCORP', models.CharField(db_column='FCCORP', default='H2ZMtM8R', max_length=8)),
                ('FCBRANCH', models.CharField(db_column='FCBRANCH', default='H2Z2kf01', max_length=8)),
                ('FCDEPT', models.CharField(db_column='FCDEPT', max_length=8)),
                ('FCSECT', models.CharField(db_column='FCSECT', max_length=8)),
                ('FCJOB', models.CharField(db_column='FCJOB', default='H2ZFfr02', max_length=8)),
                ('FCSTEP', models.CharField(db_column='FCSTEP', default='P', max_length=1)),
                ('FCBOOK', models.CharField(db_column='FCBOOK', default='JIXeqL01', max_length=8)),
                ('FCCODE', models.CharField(db_column='FCCODE', max_length=30)),
                ('FCREFNO', models.CharField(db_column='FCREFNO', max_length=35)),
                ('FCVATISOUT', models.CharField(blank=True, db_column='FCVATISOUT', default='Y', max_length=1, null=True)),
                ('FCVATTYPE', models.CharField(blank=True, db_column='FCVATTYPE', default='1', max_length=1, null=True)),
                ('FCCOOR', models.CharField(db_column='FCCOOR', max_length=8)),
                ('FCCREATEBY', models.CharField(db_column='FCCREATEBY', max_length=8)),
                ('FCCORRECTB', models.CharField(db_column='FCCORRECTB', default='$/', max_length=8)),
                ('FCEAFTERR', models.CharField(db_column='FCEAFTERR', default='E', max_length=1)),
                ('FCPROJ', models.CharField(db_column='FCPROJ', default='x/•ู((()', max_length=8)),
                ('FCAPPROVEB', models.CharField(blank=True, db_column='FCAPPROVEB', max_length=8, null=True)),
                ('FCDELICOOR', models.CharField(blank=True, db_column='FCDELICOOR', default='H2ZMtM8R', max_length=8, null=True)),
                ('FCCREATEAP', models.CharField(blank=True, db_column='FCCREATEAP', default='$/', max_length=8, null=True)),
                ('FCISPDPART', models.CharField(blank=True, db_column='FCISPDPART', default='1', max_length=1, null=True)),
                ('FDDATE', models.DateField(db_column='FDDATE')),
                ('FDDUEDATE', models.DateTimeField(auto_now=True, db_column='FDDUEDATE')),
                ('FDRECEDATE', models.DateField(auto_now=True, db_column='FDRECEDATE')),
                ('FTDATETIME', models.DateTimeField(auto_now=True, db_column='FTDATETIME')),
                ('FDAPPROVE', models.DateField(auto_now=True, db_column='FDAPPROVE')),
                ('FTLASTUPD', models.DateTimeField(auto_now=True, db_column='FTLASTUPD')),
                ('FDREQDATE', models.DateField(auto_now=True, db_column='FDREQDATE')),
                ('FNAMT', models.FloatField(blank=True, db_column='FNAMT', default='0.0', null=True)),
                ('FNAMT2', models.FloatField(blank=True, db_column='FNAMT2', default='0.0', null=True)),
                ('FNVATRATE', models.FloatField(blank=True, db_column='FNVATRATE', default='0.0', null=True)),
                ('FNVATAMT', models.FloatField(blank=True, db_column='FNVATAMT', default='0.0', null=True)),
                ('FNCREDTERM', models.FloatField(blank=True, db_column='FNCREDTERM', default='0.0', null=True)),
                ('FNAMTKE', models.FloatField(blank=True, db_column='FNAMTKE', default='0.0', null=True)),
                ('FNVATAMTKE', models.FloatField(blank=True, db_column='FNVATAMTKE', default='0.0', null=True)),
                ('FNXRATE', models.FloatField(blank=True, db_column='FNXRATE', default='0.0', null=True)),
            ],
            options={
                'db_table': 'ORDERH',
            },
        ),
        migrations.CreateModel(
            name='OrderI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FCBRANCH', models.CharField(db_column='FCBRANCH', default='H2Z2kf01', max_length=8)),
                ('FCCOOR', models.CharField(db_column='FCCOOR', max_length=8)),
                ('FCCORP', models.CharField(db_column='FCCORP', default='H2ZMtM8R', max_length=8)),
                ('FCCREATEAP', models.CharField(blank=True, db_column='FCCREATEAP', default='$/', max_length=2, null=True)),
                ('FCDATASER', models.CharField(blank=True, db_column='FCDATASER', default='$$$+', max_length=4, null=True)),
                ('FCDEPT', models.CharField(db_column='FCDEPT', max_length=8)),
                ('FCEAFTERR', models.CharField(blank=True, db_column='FCEAFTERR', default='E', max_length=1, null=True)),
                ('FCGVPOLICY', models.CharField(blank=True, db_column='FCGVPOLICY', default='1', max_length=1, null=True)),
                ('FCJOB', models.CharField(blank=True, db_column='FCJOB', default='H2ZFfr02', max_length=8, null=True)),
                ('FCLUPDAPP', models.CharField(blank=True, db_column='FCLUPDAPP', default='$/', max_length=2, null=True)),
                ('FCORDERH', models.CharField(db_column='FCORDERH', max_length=8)),
                ('FCPROD', models.CharField(db_column='FCPROD', max_length=8)),
                ('FCPRODTYPE', models.CharField(db_column='FCPRODTYPE', max_length=1)),
                ('FCPROJ', models.CharField(blank=True, db_column='FCPROJ', default='H2ZFfQ02', max_length=8, null=True)),
                ('FCREFPDTYP', models.CharField(blank=True, db_column='FCREFPDTYP', default='P', max_length=1, null=True)),
                ('FCREFTYPE', models.CharField(db_column='FCREFTYPE', max_length=2)),
                ('FCSECT', models.CharField(db_column='FCSECT', max_length=8)),
                ('FCSEQ', models.CharField(db_column='FCSEQ', max_length=4)),
                ('FCSHOWCOMP', models.CharField(db_column='FCSHOWCOMP', max_length=1)),
                ('FCSKID', models.CharField(blank=True, db_column='FCSKID', default='keWfMMal', max_length=8, null=True)),
                ('FCSTEP', models.CharField(blank=True, db_column='FCSTEP', default='P', max_length=1, null=True)),
                ('FCSTUM', models.CharField(db_column='FCSTUM', max_length=8)),
                ('FCUM', models.CharField(db_column='FCUM', max_length=8)),
                ('FCUMSTD', models.CharField(db_column='FCUMSTD', max_length=8)),
                ('FCVATISOUT', models.CharField(blank=True, db_column='FCVATISOUT', default='Y', max_length=1, null=True)),
                ('FCVATTYPE', models.CharField(blank=True, db_column='FCVATTYPE', default='1', max_length=1, null=True)),
                ('FCWHOUSE', models.CharField(blank=True, db_column='FCWHOUSE', default='H2u7qN02', max_length=8, null=True)),
                ('FDDATE', models.DateField(blank=True, db_column='FDDATE', null=True)),
                ('FDDELIVERY', models.DateField(blank=True, db_column='FDDELIVERY', null=True)),
                ('FMREMARK', models.TextField(blank=True, db_column='FMREMARK', null=True)),
                ('FNBACKQTY', models.FloatField(blank=True, db_column='FNBACKQTY', default='0.0', null=True)),
                ('FNPRICE', models.FloatField(blank=True, db_column='FNPRICE', default='0.0', null=True)),
                ('FNPRICEKE', models.FloatField(blank=True, db_column='FNPRICEKE', default='0.0', null=True)),
                ('FNQTY', models.FloatField(blank=True, db_column='FNQTY', default='0.0', null=True)),
                ('FNUMQTY', models.FloatField(blank=True, db_column='FNUMQTY', default='0.0', null=True)),
                ('FNVATAMT', models.FloatField(blank=True, db_column='FNVATAMT', default='0.0', null=True)),
                ('FNVATRATE', models.FloatField(blank=True, db_column='FNVATRATE', default='0.0', null=True)),
                ('FNXRATE', models.FloatField(blank=True, db_column='FNXRATE', default='0.0', null=True)),
                ('FTDATETIME', models.DateTimeField(auto_now=True, db_column='FTDATETIME')),
                ('FTLASTUPD', models.DateTimeField(auto_now=True, db_column='FTLASTUPD')),
            ],
            options={
                'db_table': 'ORDERI',
            },
        ),
        migrations.CreateModel(
            name='PROD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FCSKID', models.CharField(blank=True, db_column='FCSKID', default='MBaSspMB', max_length=8, null=True)),
                ('FCCODE', models.CharField(db_column='FCCODE', max_length=30)),
                ('FCNAME', models.CharField(db_column='FCNAME', max_length=30)),
                ('FCPDGRP', models.CharField(db_column='FCPDGRP', max_length=30)),
                ('FCTYPE', models.CharField(db_column='FCTYPE', max_length=30)),
            ],
            options={
                'db_table': 'PROD',
            },
        ),
        migrations.CreateModel(
            name='SECT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FCSKID', models.CharField(blank=True, db_column='FCSKID', default='xyHu9ods', max_length=8, null=True)),
                ('FCCODE', models.CharField(db_column='FCCODE', max_length=30)),
                ('FCNAME', models.CharField(db_column='FCNAME', max_length=30)),
            ],
            options={
                'db_table': 'SECT',
            },
        ),
    ]