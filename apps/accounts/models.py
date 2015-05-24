import random
import string
import datetime
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from apps.posts.models import *

class UserProfiles(models.Model):

    user = models.OneToOneField(User,related_name='user_profiles')
    mobile = models.IntegerField('Mobile')
    skypeid = models.CharField(('Skype ID'),max_length=150)
    country = CountryField()
    smsalert = models.BooleanField('Sms Alert', default=False)
    emailalert = models.BooleanField('Email Alert', default=False)
    otp = models.IntegerField('OTP',null=True,blank=True)
    token = models.CharField('Token',max_length=200,null=True,blank=True)

    def __unicode(self):
        return u'%s' %(self.user)

    def random_key(self):
        alphabet = [c for c in string.letters + string.digits if ord(c) < 128]
        return ''.join([random.choice(alphabet) for x in xrange(30)])

    def save(self,*args,**kwargs):
        super(UserProfiles, self).save(*args, **kwargs)
        self.token=self.random_key()
        super(UserProfiles, self).save(*args, ** kwargs)

    class Meta:
        verbose_name = 'User Profile'

class UserInterests(models.Model):
    user = models.OneToOneField(User,related_name='user_interests')
    interests = models.ManyToManyField(Posts)

    def __unicode__(self):
        return u'%s'%(self.user)

class SubscriptionPlan(models.Model):
    title = models.CharField('Name',max_length=100)
    post_requirement = models.IntegerField('Post Requirement')
    view_requirement = models.IntegerField('View Requirement')
    view_contact = models.IntegerField('View Contact')
    show_interest = models.IntegerField('Show Interest')
    contact = models.BooleanField('Displays Contact Detail of Person who Showed Interest',default=False)

    def __unicode__(self):
        return self.title

class UserSubscriptions(models.Model):
    user = models.ForeignKey(User,related_name='user_plan')
    plan = models.ForeignKey(SubscriptionPlan,related_name='subscribe_plan')
    start_date = models.DateTimeField('Start Date',auto_now=True)
    expiry_date = models.DateTimeField('Expiry Date',)

    def __unicode__(self):
        return u'%s'%(self.user)
