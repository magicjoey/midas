import datetime
import json

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail

import meta
from spider.bank_maintain_task import crawl


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


class AccountType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32, blank=False, null=False)
    is_deposit = models.CharField(max_length=1, blank=False, null=False)
    owner_id = models.IntegerField(blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True, default=timezone.now())
    type = models.CharField(max_length=32, blank=False, null=False)

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


class AccountFlow(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    account_id = models.ForeignKey(Account, max_length=12, on_delete=models.DO_NOTHING,
                                   verbose_name="账户",
                                   db_column="account_id", related_name='account_fk')
    sub_id = models.ForeignKey(AccountSub, max_length=12, on_delete=models.DO_NOTHING,
                               verbose_name="子账户",
                               db_column="sub_id", related_name='sub_account_fk')
    amount = models.FloatField()
    before_balance = models.FloatField(blank=True, null=True)
    after_balance = models.FloatField(blank=True, null=True)
    operate_type = models.CharField(max_length=10, blank=True, null=True)
    direction = models.CharField(max_length=1, blank=True, null=True)
    memo = models.CharField(max_length=100, blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True, default=timezone.now())
    gmt_update = models.DateTimeField(blank=True, null=True, default=timezone.now())
    trade_name = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=128, blank=True, null=True)
    gmt_occur = models.DateTimeField(blank=True, null=True, default=timezone.now())

    class Meta:
        managed = False
        db_table = 'tb_account_flow'


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


class BankMaintain(models.Model):
    url = models.CharField(max_length=128, blank=True, null=True)
    title = models.CharField(max_length=128, blank=True, null=True)
    release_date = models.CharField(max_length=128, blank=True, null=True)
    full_title = models.CharField(max_length=256, blank=True, null=True)
    content = models.CharField(max_length=5000, blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True, default=timezone.now())

    class Meta:
        managed = False
        db_table = 'tb_bank_maintain'


class Gold(models.Model):
    type = models.CharField(max_length=10, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    gmt_create = models.DateTimeField(blank=True, null=True, default=timezone.now())
    max_price = models.FloatField(blank=True, null=True)
    min_price = models.FloatField(blank=True, null=True)
    yes_price = models.FloatField(blank=True, null=True)
    open_price = models.FloatField(blank=True, null=True)
    total_vol = models.FloatField(blank=True, null=True)
    limit = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_gold'  # @sched.interval_schedule(seconds=100)


def bank_notify_crawl():
    data = crawl()
    # 发送邮件
    content = ""
    for key in data.keys():
        for single in data.get(key):
            try:
                bank_maintain = BankMaintain.objects.get(url=single['url'], full_title=single['full-title'])
            except BankMaintain.DoesNotExist:
                bank_maintain = BankMaintain(url=single['url'], title=single['title'],
                                             full_title=single['full-title'], content=single['content'],
                                             release_date=single['release-date'])
                bank_maintain.save()
            if (timezone.now() - bank_maintain.gmt_create).days > 7:
                continue
            content += "\n\n链接:" + single['url'] + "\n,标题:" + single['title'] + ",发布日期:" + single[
                'release-date'] + ",\n详情如下:\n" + single['content']
    result = send_mail('银行渠道维护公告-爬虫', content, 'dragonsmaug@126.com',
                       ['1306164951@qq.com', '475583762@qq.com', '841035336@qq.com'], fail_silently=False,
                       html_message='')


# 黄金同步
def gold_sync():
    try:
        url = "http://web.juhe.cn:8080/finance/gold/shgold?v=&key=5465b4584fbdc8155b2693ae9fee2ac0"
        resp = requests.get(url, timeout=3, verify=False)
        result = json.loads(resp.content.decode())
        if result['error_code'] == 0:
            for entry in result['result']:
                for key in entry:
                    if entry[key]['variety'] == "Au100g":
                        current_time = datetime.datetime.strptime(entry[key]['time'], '%Y-%m-%d %H:%M:%S')
                        gold = Gold(type="GOLD", time=current_time, price=float(entry[key]['latestpri'])
                                    , max_price=float(entry[key]['maxpri']), min_price=float(entry[key]['minpri']),
                                    yes_price=float(entry[key]['yespri']),
                                    open_price=float(entry[key]['openpri']),
                                    total_vol=float(entry[key]['totalvol']), limit=entry[key]['limit'])
                        gold.save()
        return resp
    except:
        pass

def income_distribute():
    try:
        account_list = Account.objects.all()
        account_type = "bonus"
        for account in account_list:
            left_amount = account.balance
            try:
                account_sub_list = AccountSub.objects.filter(account_id_id=account.account_id)
                for account_sub in account_sub_list:
                    if account_sub.return_rate is not None and account_sub.return_rate != 0:
                        bonus(account.account_id, account_sub.id, account_sub.return_rate * account_sub.balance,
                              account_sub.user_id, account_type, str(meta.get_yesterday()) + '收益发放', "收益")
                    left_amount = account.balance - account_sub.balance
            except AccountSub.DoesNotExist:
                pass
            bonus(account.account_id, None, account.return_rate * left_amount,
                  account.user_id, account_type, str(meta.get_yesterday()) + '收益发放', "收益")
        print("收益发放结束")
    except:
        pass

sched = BackgroundScheduler()
sched.add_job(bank_notify_crawl, 'cron', second='0', minute='40', hour='9', )
sched.add_job(income_distribute, 'cron', second='0', minute='0', hour='2', )
sched.add_job(gold_sync, 'cron', second='0', minute='0', hour='9',)
sched.start()


def bonus(account_id, sub_id, amount, balance, user_id, account_type, memo, label):
    try:
        after_balance = meta.calc_after_amount(account_type, balance,
                                               amount)
        flow = AccountFlow(user_id=user_id, account_id_id=account_id, sub_id_id=sub_id, amount=amount,
                           before_balance=balance,
                           after_balance=after_balance,
                           operate_type=account_type,
                           direction=meta.get_direction(account_type, False),
                           memo=memo,
                           label=label)
        if sub_id is None:
            account = Account.objects.get(account_id=account_id, user_id=user_id)
            account.balance = after_balance
            account.gmt_modified = timezone.now()
            account.save()
        else:
            account_sub = AccountSub.objects.get(account_id_id=account_id, id=sub_id, user_id=user_id)
            account_sub.balance = after_balance
            account_sub.gmt_modified = timezone.now()
            account_sub.save()
        flow.save()
    except:
        pass