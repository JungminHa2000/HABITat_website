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
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
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
    furniture_name = models.TextField(blank=True, null=True)
    price = models.BigIntegerField(blank=True, null=True)
    furniture_png = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'furniture_catalog'


class GoalInfo(models.Model):
    goal_id = models.BigAutoField(primary_key=True)
    goal_desc = models.CharField(max_length=255, blank=True, null=True)
    bank = models.BigIntegerField(blank=True, null=True)
    inventory = models.TextField(blank=True, null=True)
    room_info = models.TextField(blank=True, null=True)
    vis = models.CharField(max_length=255, blank=True, null=True)
    last_checked = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'goal_info'


class Goals(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('UserData', models.DO_NOTHING)
    goal_id = models.PositiveBigIntegerField()

    class Meta:
        managed = False
        db_table = 'goals'


class Reminders(models.Model):
    id = models.BigAutoField(primary_key=True)
    task = models.ForeignKey('Tasks', models.DO_NOTHING, blank=True, null=True)
    day_of_week = models.TextField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reminders'


class Report(models.Model):
    # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    no_field = models.BigAutoField(db_column='No.', primary_key=True)
    date_reported = models.DateField(blank=True, null=True)
    reportee_id = models.BigIntegerField(blank=True, null=True)
    reportee_username = models.TextField(blank=True, null=True)
    reporter_id = models.PositiveBigIntegerField(blank=True, null=True)
    reporter_username = models.TextField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    admin_responded = models.BigIntegerField(blank=True, null=False)

    class Meta:
        managed = False
        db_table = 'report'


class Requests(models.Model):
    # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    no_field = models.BigAutoField(db_column='No.', primary_key=True)
    date_requested = models.DateField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    user_name = models.TextField(blank=True, null=True)
    goal = models.ForeignKey(
        GoalInfo, models.DO_NOTHING, blank=True, null=True)
    goal_desc = models.TextField(blank=True, null=True)
    task_id = models.BigIntegerField(blank=True, null=True)
    task_desc = models.TextField(blank=True, null=True)
    assigned_reward = models.PositiveBigIntegerField(blank=True, null=True)
    requested_reward = models.PositiveBigIntegerField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    admin_responded = models.BigIntegerField(blank=True, null=False)

    class Meta:
        managed = False
        db_table = 'requests'


class Tasks(models.Model):
    goal = models.ForeignKey(
        GoalInfo, models.DO_NOTHING, blank=True, null=True)
    task_id = models.BigAutoField(primary_key=True)
    task_desc = models.TextField(blank=True, null=True)
    reward = models.BigIntegerField(blank=True, null=True)
    last_datetime = models.TextField(blank=True, null=True)
    sunday = models.TimeField(blank=True, null=True)
    monday = models.TimeField(blank=True, null=True)
    tuesday = models.TimeField(blank=True, null=True)
    wednesday = models.TimeField(blank=True, null=True)
    thursday = models.TimeField(blank=True, null=True)
    friday = models.TimeField(blank=True, null=True)
    saturday = models.TimeField(blank=True, null=True)
    completed_history = models.TextField(blank=True, null=True)
    votes = models.TextField(blank=True, null=True)
    num_votes = models.BigIntegerField(blank=True, null=True)
    streak = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tasks'


class UserData(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    friends_info = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    salt = models.CharField(max_length=255, blank=True, null=True)
    incoming_friend_req = models.TextField(blank=True, null=True)
    outgoing_friend_req = models.TextField(blank=True, null=True)
    gem = models.BigIntegerField(blank=True, null=True)
    num_reported = models.BigIntegerField(blank=True, null=True)
    banned = models.BigIntegerField(blank=True, null=False)

    class Meta:
        managed = False
        db_table = 'user_data'
