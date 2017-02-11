from django.db import models
from django.utils import timezone


class AccountCard(models.Model):
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
        db_table = 'tb_account_card'


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
    trade_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_account_flow'


class AccountType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32, blank=False, null=False)
    is_deposit = models.CharField(max_length=1, blank=False, null=False)
    owner_id = models.IntegerField(blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True, default=timezone.now())

    class Meta:
        managed = False
        db_table = 'tb_account_type'


class Bank(models.Model):
    bank_code = models.CharField(primary_key=True, max_length=5)
    bank_name = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_bank'


class CreditCard(models.Model):
    id = models.IntegerField(primary_key=True)
    bank_code = models.CharField(max_length=10, blank=True, null=True)
    card_name = models.CharField(max_length=30, blank=True, null=True)
    card_type = models.CharField(max_length=10, blank=True, null=True)
    card_face = models.CharField(max_length=256, blank=True, null=True)
    apply_url = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_credit_card'


class CreditCardActivity(models.Model):
    id = models.IntegerField(primary_key=True)
    card_id = models.IntegerField(blank=True, null=True)
    activity_name = models.CharField(max_length=30, blank=True, null=True)
    link_url = models.CharField(max_length=30, blank=True, null=True)
    participate_condition = models.CharField(max_length=256, blank=True, null=True)
    activity_type = models.CharField(max_length=1, blank=True, null=True)
    gmt_start = models.DateField(blank=True, null=True)
    gmt_end = models.DateField(blank=True, null=True)
    limit_condition = models.CharField(max_length=30, blank=True, null=True)
    prize = models.CharField(max_length=200, blank=True, null=True)
    attention = models.CharField(max_length=200, blank=True, null=True)
    prize_evaluate = models.CharField(max_length=50, blank=True, null=True)
    simple_strategy = models.CharField(max_length=300, blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True)
    gmt_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_credit_card_activity'


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
    owner_id = models.IntegerField(blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True, default=timezone.now())
    memo = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_platform'


class PlatformProduct(models.Model):
    product_id = models.AutoField(primary_key=True)
    platform_id = models.IntegerField(blank=True, null=True)
    product_name = models.CharField(max_length=32, blank=True, null=True)
    repay_type = models.CharField(max_length=10, blank=True, null=True)
    interest_rate = models.FloatField(blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True, default=timezone.now())

    class Meta:
        managed = False
        db_table = 'tb_platform_product'


class Account(models.Model):
    account_id = models.IntegerField(primary_key=True, blank=True)
    account_name = models.CharField(max_length=32, blank=True, null=True)
    user_id = models.IntegerField(blank=False, null=False)
    platform = models.ForeignKey(Platform, max_length=12, on_delete=models.DO_NOTHING,
                                 verbose_name="平台",
                                 db_column="platform", related_name='platform_fk')
    account_type = models.ForeignKey(AccountType, max_length=12, on_delete=models.DO_NOTHING,
                                     verbose_name="账户类型",
                                     db_column="account_type", related_name='account_type_fk')
    balance = models.FloatField(blank=True, null=True)
    usage = models.CharField(max_length=20, blank=True, null=True)
    gmt_start = models.DateField(blank=True, null=True)
    cycle = models.IntegerField(blank=True, null=True)
    gmt_end = models.DateField(blank=True, null=True)
    return_rate = models.FloatField(blank=True, null=True)
    memo = models.CharField(max_length=100, blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True, default=timezone.now())
    gmt_modified = models.DateTimeField(blank=True, null=True, default=timezone.now())
    status = models.CharField(max_length=1, blank=True, null=True, default='N')
    weight = models.IntegerField(blank=True, null=True, default='0')

    class Meta:
        managed = False
        db_table = 'tb_account'


class AccountSub(models.Model):
    id = models.IntegerField(primary_key=True)
    account_id = models.ForeignKey(Account, max_length=11, on_delete=models.DO_NOTHING,
                                   verbose_name="主账户",
                                   db_column="account_id", related_name='account_pk')
    account_name = models.CharField(max_length=32, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    memo = models.CharField(max_length=64, blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    return_rate = models.FloatField(blank=True, null=True)
    redeem_type = models.CharField(max_length=1, blank=True, null=True)
    gmt_start = models.DateField(blank=True, null=True)
    gmt_end = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True, default=timezone.now())
    gmt_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_account_sub'


class AccountDeposit(models.Model):
    account_id = models.ForeignKey(Account, max_length=11, on_delete=models.DO_NOTHING,
                                   verbose_name="主账户",
                                   db_column="account_id")
    user_id = models.IntegerField(blank=True, null=True)
    sub_id = models.IntegerField(blank=True, null=True)
    account_type = models.IntegerField(blank=True, null=True)
    deposit_type = models.CharField(max_length=1, blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True, default=timezone.now())
    gmt_modified = models.DateTimeField(blank=True, null=True)
    day = models.CharField(max_length=32, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    base = models.FloatField(blank=True, null=True)
    deposit_rate = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_account_deposit'


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


class SmsRecord(models.Model):
    mobile_no = models.CharField(max_length=11, blank=True, null=True)
    content = models.CharField(max_length=256, blank=True, null=True)
    verify_code = models.CharField(max_length=12, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_sms_record'


class SmsTemplate(models.Model):
    type = models.CharField(primary_key=True, max_length=12)
    content = models.CharField(max_length=256, blank=True, null=True)
    gmt_create = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tb_sms_template'


class SmsType(models.Model):
    type = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_sms_type'


class Config(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)
    content = models.CharField(max_length=256, blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True)
    gmt_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_config'


class RateParam(models.Model):
    id = models.IntegerField(primary_key=True)
    half_minute = models.IntegerField()
    five_minutes = models.IntegerField()
    one_day = models.IntegerField()
