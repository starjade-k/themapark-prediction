# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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


class PreEntrance(models.Model):
    pe_idx = models.BigAutoField(primary_key=True)
    theme_name = models.CharField(max_length=30, blank=True, null=True)
    std_date = models.DateField(blank=True, null=True)
    ent_num = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pre_entrance'


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
