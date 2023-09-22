# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

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
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FurnitureCatalog(models.Model):
    furniture_id = models.BigAutoField(primary_key=True)
    furniture_name = models.CharField(max_length=255)
    furniture_pack = models.CharField(max_length=255)
    data = models.TextField()
    price = models.BigIntegerField()

    class Meta:
        db_table = 'furniture_catalog'


class GoalInfo(models.Model):
    goal_id = models.BigAutoField(primary_key=True)
    goal_desc = models.CharField(max_length=255)
    bank = models.PositiveBigIntegerField()
    inventory = models.JSONField(blank=True, null=True)
    room_info = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'goal_info'


class Goals(models.Model):
    user_id = models.PositiveBigIntegerField()
    goal = models.ForeignKey(GoalInfo, models.DO_NOTHING)

    class Meta:
        db_table = 'goals'


class Reminders(models.Model):
    task_id = models.PositiveBigIntegerField()
    day_of_week = models.CharField(max_length=255)
    time = models.TimeField(blank=True, null=True)

    class Meta:
        db_table = 'reminders'


class Report(models.Model):
    no_field = models.BigAutoField(db_column='No.', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    reportee_id = models.BigIntegerField()
    reporter_id = models.PositiveBigIntegerField()
    reason = models.CharField(max_length=255)

    class Meta:
        db_table = 'report'


class Requests(models.Model):
    no_field = models.BigAutoField(db_column='No.', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    date_requested = models.DateField()
    user_id = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    goal_id = models.BigIntegerField()
    goal_desc = models.CharField(max_length=255)
    task_id = models.BigIntegerField()
    task_desc = models.CharField(max_length=255)
    assigned_reward = models.PositiveBigIntegerField()
    requested_reward = models.PositiveBigIntegerField()
    reason = models.CharField(max_length=255)
    class Meta:
        db_table = 'requests'


class Tasks(models.Model):
    goal_id = models.PositiveBigIntegerField()
    task_id = models.BigAutoField(primary_key=True)
    task_desc = models.CharField(max_length=255)
    reward = models.BigIntegerField()

    class Meta:
        db_table = 'tasks'


class UserData(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    friends_info = models.TextField(blank=True, null=True)
    password = models.TextField()

    class Meta:
        db_table = 'user_data'
