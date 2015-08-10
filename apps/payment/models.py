from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):

    TYPES = (
        ('0', 'Credit Card'),
        ('1', 'Paypal')
    )

    user = models.OneToOneField(User, related_name='user_payment')
    payment_type = models.CharField('Payment Type', choices=TYPES, max_length=150, null=True, blank=True)
    plan = models.CharField('Plans', max_length=150)
    amount = models.IntegerField('Amount Payed')
    date = models.DateField('Date')
    time = models.TimeField('Time')

    def __unicode__(self):
        return u'%s' % self.user