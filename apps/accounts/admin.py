from django.contrib import admin
from apps.accounts.models import *

admin.site.register(UserProfiles)

class InterestAdmin(admin.ModelAdmin):
    filter_horizontal = ('interests',)
admin.site.register(UserInterests, InterestAdmin)
admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscriptions)