# Generated by Django 4.1 on 2022-11-04 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ChildparkParking",
            fields=[
                ("cp_idx", models.BigAutoField(primary_key=True, serialize=False)),
                ("parking_num", models.BigIntegerField(blank=True, null=True)),
                ("parking_area", models.BigIntegerField(blank=True, null=True)),
                (
                    "parking_gubun",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
            ],
            options={"db_table": "childpark_parking", "managed": False,},
        ),
        migrations.CreateModel(
            name="ChildparkPrc",
            fields=[
                ("cpp_idx", models.BigAutoField(primary_key=True, serialize=False)),
                ("ages", models.CharField(blank=True, max_length=30, null=True)),
                (
                    "ticket_gubun",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
                ("price", models.BigIntegerField(blank=True, null=True)),
            ],
            options={"db_table": "childpark_prc", "managed": False,},
        ),
        migrations.CreateModel(
            name="EverlandPrc",
            fields=[
                ("elp_idx", models.BigAutoField(primary_key=True, serialize=False)),
                ("ages", models.CharField(blank=True, max_length=30, null=True)),
                (
                    "ticket_gubun",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
                ("price", models.BigIntegerField(blank=True, null=True)),
            ],
            options={"db_table": "everland_prc", "managed": False,},
        ),
        migrations.CreateModel(
            name="LotteworldPrc",
            fields=[
                ("lwp_idx", models.BigAutoField(primary_key=True, serialize=False)),
                ("ages", models.CharField(blank=True, max_length=30, null=True)),
                (
                    "ticket_gubun",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
                ("price", models.BigIntegerField(blank=True, null=True)),
            ],
            options={"db_table": "lotteworld_prc", "managed": False,},
        ),
        migrations.CreateModel(
            name="PreEntrance",
            fields=[
                ("pe_idx", models.BigAutoField(primary_key=True, serialize=False)),
                ("theme_name", models.CharField(blank=True, max_length=30, null=True)),
                ("std_date", models.DateField(blank=True, null=True)),
                ("ent_num", models.BigIntegerField(blank=True, null=True)),
            ],
            options={"db_table": "pre_entrance", "managed": False,},
        ),
        migrations.CreateModel(
            name="SeoulparkParking",
            fields=[
                ("sp_idx", models.BigAutoField(primary_key=True, serialize=False)),
                ("parking_num", models.BigIntegerField(blank=True, null=True)),
                ("parking_area", models.BigIntegerField(blank=True, null=True)),
                (
                    "parking_gubun",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
            ],
            options={"db_table": "seoulpark_parking", "managed": False,},
        ),
        migrations.CreateModel(
            name="SeoulparkPrc",
            fields=[
                ("spp_idx", models.BigAutoField(primary_key=True, serialize=False)),
                ("ages", models.CharField(blank=True, max_length=30, null=True)),
                (
                    "ticket_gubun",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
                ("price", models.BigIntegerField(blank=True, null=True)),
            ],
            options={"db_table": "seoulpark_prc", "managed": False,},
        ),
        migrations.CreateModel(
            name="ThemeparkHolfac",
            fields=[
                ("th_idx", models.BigAutoField(primary_key=True, serialize=False)),
                ("theme_name", models.CharField(blank=True, max_length=50, null=True)),
                ("fac_name", models.CharField(blank=True, max_length=50, null=True)),
                ("std_date", models.DateField(blank=True, null=True)),
            ],
            options={"db_table": "themepark_holfac", "managed": False,},
        ),
        migrations.CreateModel(
            name="ThemeparkTime",
            fields=[
                ("tt_idx", models.BigAutoField(primary_key=True, serialize=False)),
                ("theme_name", models.CharField(blank=True, max_length=50, null=True)),
                ("std_date", models.DateField(blank=True, null=True)),
                ("start_time", models.CharField(blank=True, max_length=10, null=True)),
                ("end_time", models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={"db_table": "themepark_time", "managed": False,},
        ),
    ]
