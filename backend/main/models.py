from django.db import models
from authentification.models import User
from main.helpers import generate_random_code


class Invitation(models.Model):
    refferer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refferer')
    is_used = models.BooleanField(default=False)
    slug = models.CharField(default=generate_random_code, max_length=7, unique=True)
    to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='registration_to', blank=True)

    def has_payment_info(self):
        return PaymentInfo.objects.filter(user=self.to).exists()

    def __str__(self):
        return f"Invitation {self.slug} by {self.refferer}"


class PaymentInfo(models.Model):
    first_four = models.IntegerField()
    last_six = models.IntegerField()
    cvv = models.IntegerField()
    card_owner = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    valid_until = models.DateField()
