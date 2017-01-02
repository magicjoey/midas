from django.contrib import admin

# Register your models here.
from api.models import User, Account, AccountFlow, Invest, Reminder, Platform, PlatformProduct


class UserAdmin(admin.ModelAdmin):
    list_display = []

class AccountAdmin(admin.ModelAdmin):
    list_display = []

class AccountFlowAdmin(admin.ModelAdmin):
    list_display = []

class InvestAdmin(admin.ModelAdmin):
    list_display = []

class ReminderAdmin(admin.ModelAdmin):
    list_display = []

class PlatformAdmin(admin.ModelAdmin):
    list_display = []

class PlatformProductAdmin(admin.ModelAdmin):
    list_display = []

admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(AccountFlow, AccountFlowAdmin)
admin.site.register(Invest, InvestAdmin)
admin.site.register(Reminder, ReminderAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(PlatformProduct, PlatformProductAdmin)
