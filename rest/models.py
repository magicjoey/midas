from django.db import models

# Create your models here.
class Account(models.Model):
    account_id = models.IntegerField(primary_key=True)
    account_name = models.CharField(max_length=32, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    platform_id = models.IntegerField(blank=True, null=True)
    account_type = models.CharField(max_length=5, blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True)
    gmt_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_account'


class AccountFlow(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    account_id = models.IntegerField(blank=True, null=True)
    amount = models.FloatField()
    before_balance = models.FloatField(blank=True, null=True)
    after_balance = models.FloatField(blank=True, null=True)
    operate_type = models.CharField(max_length=10, blank=True, null=True)
    direction = models.CharField(max_length=1, blank=True, null=True)
    memo = models.CharField(max_length=100, blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True)
    gmt_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_account_flow'


class Invest(models.Model):
    invest_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    product_id = models.IntegerField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=32)
    memo = models.CharField(max_length=100, blank=True, null=True)
    dealine_day = models.DateField()
    gmt_create = models.DateTimeField(blank=True, null=True)
    gmt_modified = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_invest'


class Platform(models.Model):
    platform_id = models.AutoField(primary_key=True)
    platform_name = models.CharField(max_length=32, blank=True, null=True)
    owner_type = models.CharField(max_length=5)
    owner_id = models.IntegerField(blank=True, null=True)
    gmt_create = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tb_platform'


class PlatformProduct(models.Model):
    product_id = models.AutoField(primary_key=True)
    platform_id = models.IntegerField(blank=True, null=True)
    product_name = models.CharField(max_length=32, blank=True, null=True)
    repay_type = models.CharField(max_length=10, blank=True, null=True)
    interest_rate = models.FloatField(blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_platform_product'


class Reminder(models.Model):
    reminder_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    content = models.CharField(max_length=256, blank=True, null=True)
    reminder_type = models.CharField(max_length=5, blank=True, null=True)
    gmt_notify = models.DateTimeField(blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_reminder'


class RepayType(models.Model):
    repay_type = models.CharField(primary_key=True, max_length=10)
    repay_name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_repay_type'


class User(models.Model):
    user_name = models.CharField(unique=True, max_length=32, blank=True, null=True)
    password = models.CharField(max_length=32, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    is_admin = models.IntegerField(blank=True, null=True)
    is_delete = models.IntegerField(blank=True, null=True)
    nick_name = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=8)
    avatar = models.CharField(max_length=128, blank=True, null=True)
    introduction = models.CharField(max_length=128, blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    birthday = models.CharField(max_length=10, blank=True, null=True)
    alipay = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=8, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)
    gmt_login = models.DateTimeField(blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True)
    gmt_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_user'