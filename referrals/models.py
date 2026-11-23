from django.db import models
from users.models import User


class Referral(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='referral'
    )

    referral_code = models.CharField(
        max_length=20,
        unique=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.referral_code}"


class ReferralUsage(models.Model):

    referral = models.ForeignKey(
        Referral,
        on_delete=models.CASCADE,
        related_name='usages'
    )

    referred_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='used_referral'
    )

    reward_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referred_user.email} used {self.referral.referral_code}"    