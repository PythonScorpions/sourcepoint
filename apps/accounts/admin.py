from django.contrib import admin
from apps.accounts.models import *

admin.site.register(UserProfiles)

admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscriptions)

class IpAdmin(admin.ModelAdmin):
    filter_horizontal = ('posts',)

admin.site.register(IpTracker, IpAdmin)
admin.site.register(InterestOfUsers)