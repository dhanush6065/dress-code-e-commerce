from django.contrib import admin
from .models import Referral, ReferralUsage


admin.site.register(Referral)
admin.site.register(ReferralUsage)