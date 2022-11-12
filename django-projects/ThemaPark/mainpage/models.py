# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class ChildparkParking(models.Model):
    cp_idx = models.BigAutoField(primary_key=True)
    parking_num = models.BigIntegerField(blank=True, null=True)
    parking_area = models.BigIntegerField(blank=True, null=True)
    parking_gubun = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'childpark_parking'


class ChildparkPrc(models.Model):
    cpp_idx = models.BigAutoField(primary_key=True)
    ages = models.CharField(max_length=30, blank=True, null=True)
    ticket_gubun = models.CharField(max_length=30, blank=True, null=True)
    price = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'childpark_prc'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EverlandPrc(models.Model):
    elp_idx = models.BigAutoField(primary_key=True)
    ages = models.CharField(max_length=30, blank=True, null=True)
    ticket_gubun = models.CharField(max_length=30, blank=True, null=True)
    price = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'everland_prc'


class LotteworldPrc(models.Model):
    lwp_idx = models.BigAutoField(primary_key=True)
    ages = models.CharField(max_length=30, blank=True, null=True)
    ticket_gubun = models.CharField(max_length=30, blank=True, null=True)
    price = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lotteworld_prc'


class PreAirWeather(models.Model):
    paw_idx = models.BigAutoField(primary_key=True)
    theme_name = models.CharField(max_length=30, blank=True, null=True)
    std_date = models.DateField(blank=True, null=True)
    high_temp = models.FloatField(blank=True, null=True)
    low_temp = models.FloatField(blank=True, null=True)
    diff_temp = models.FloatField(blank=True, null=True)
    rain_amount = models.FloatField(blank=True, null=True)
    avg_wind = models.FloatField(blank=True, null=True)
    high_wind = models.FloatField(blank=True, null=True)
    pm10 = models.BigIntegerField(blank=True, null=True)
    pm25 = models.BigIntegerField(blank=True, null=True)
    weather_img = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pre_air_weather'


class PreEntrance(models.Model):
    pe_idx = models.BigAutoField(primary_key=True)
    theme_name = models.CharField(max_length=30, blank=True, null=True)
    std_date = models.DateField(blank=True, null=True)
    ent_num = models.BigIntegerField(blank=True, null=True)
    congestion = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pre_entrance'


class PreEvent(models.Model):
    pe_idx = models.BigAutoField(primary_key=True)
    theme_name = models.CharField(max_length=50, blank=True, null=True)
    std_date = models.DateField(blank=True, null=True)
    event_ox = models.BigIntegerField(blank=True, null=True)
    event_name = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pre_event'


class PreNavi(models.Model):
    pn_idx = models.BigAutoField(primary_key=True)
    theme_name = models.CharField(max_length=50, blank=True, null=True)
    navi_src_num = models.BigIntegerField(blank=True, null=True)
    congestion = models.BigIntegerField(blank=True, null=True)
    std_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pre_navi'


class SeoulparkParking(models.Model):
    sp_idx = models.BigAutoField(primary_key=True)
    parking_num = models.BigIntegerField(blank=True, null=True)
    parking_area = models.BigIntegerField(blank=True, null=True)
    parking_gubun = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seoulpark_parking'


class SeoulparkPrc(models.Model):
    spp_idx = models.BigAutoField(primary_key=True)
    ages = models.CharField(max_length=30, blank=True, null=True)
    ticket_gubun = models.CharField(max_length=30, blank=True, null=True)
    price = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seoulpark_prc'


class ThemeparkHolfac(models.Model):
    th_idx = models.BigAutoField(primary_key=True)
    theme_name = models.CharField(max_length=50, blank=True, null=True)
    fac_name = models.CharField(max_length=50, blank=True, null=True)
    std_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'themepark_holfac'


class ThemeparkTime(models.Model):
    tt_idx = models.BigAutoField(primary_key=True)
    theme_name = models.CharField(max_length=50, blank=True, null=True)
    std_date = models.DateField(blank=True, null=True)
    start_time = models.CharField(max_length=10, blank=True, null=True)
    end_time = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'themepark_time'
