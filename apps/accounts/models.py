import random
import string
import datetime
from django.contrib.sites.models import Site
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from apps.posts.models import *

class UserProfiles(models.Model):

    user = models.OneToOneField(User, related_name='user_profiles')
    mobile = models.BigIntegerField('Mobile', null=True, blank=True)
    skypeid = models.CharField('Skype ID',max_length=150, null=True, blank=True)
    country = CountryField()
    smsalert = models.BooleanField('Sms Alert', default=False)
    emailalert = models.BooleanField('Email Alert', default=False)
    otp = models.IntegerField('OTP', null=True, blank=True)
    token = models.CharField('Token', max_length=200, null=True, blank=True)
    contact_viewes = models.BigIntegerField('Total Contact Viewes', null=True, blank=True)
    email_verify = models.BooleanField('Email Verified', default=False)
    mobile_verify = models.BooleanField('Mobile Verified', default=False)

    def __unicode__(self):
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


class SubscriptionPlan(models.Model):
    title = models.CharField('Name', max_length=100)
    post_requirement = models.IntegerField('Post Requirement')
    view_requirement = models.IntegerField('View Requirement')
    view_contact = models.IntegerField('View Contact')
    show_interest = models.IntegerField('Show Interest')
    contact = models.BooleanField('Displays Contact Detail of Person who Showed Interest', default=False)
    price = models.IntegerField('Price', default=0)
    free_plan = models.BooleanField(default=False)
    active = models.BooleanField('Active', default=True)

    def __unicode__(self):
        return self.title


class UserSubscriptions(models.Model):
    user = models.ForeignKey(User, related_name='user_plan')
    plan = models.ForeignKey(SubscriptionPlan, related_name='subscribe_plan')
    post_requirement = models.IntegerField('Post Requirement')
    view_requirement = models.IntegerField('View Requirement')
    view_contact = models.IntegerField('View Contact')
    show_interest = models.IntegerField('Show Interest')
    start_date = models.DateTimeField('Start Date', auto_now=True)
    expiry_date = models.DateTimeField('Expiry Date',)

    def __unicode__(self):
        return u'%s'%(self.user)


class TermsandCondition(models.Model):
    site = models.OneToOneField(Site)
    description = models.TextField('Description1')
    description2 = models.TextField('Description2')

    def __unicode__(self):
        return u'%s' % self.site

class Reports(models.Model):
    site = models.OneToOneField(Site)
    daily_report = models.FileField(upload_to='files/', null=True, blank=True)
    monthly_report = models.FileField(upload_to='files/', null=True, blank=True)

class IpTracker(models.Model):
    ip = models.IPAddressField()
    user = models.ForeignKey(User, related_name='user_track')
    posts = models.ManyToManyField(Posts, related_name='post_track')
    view_count = models.IntegerField('View Count', default=0)
    intersets = models.ManyToManyField(Posts, null=True, blank=True, through='UserInterests')
    interest_count = models.IntegerField('Total Interest Shown', default=0)
    post_count = models.IntegerField('Total Post Added', default=0)
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.user


class UserInterests(models.Model):
    user_post = models.ForeignKey(Posts, null=True, blank=True, related_name='interest_post')
    tracker = models.ForeignKey(IpTracker, null=True, blank=True, related_name='interest_track')
    date = models.DateTimeField(auto_now=True)


class InterestOfUsers(models.Model):
    post_name = models.ForeignKey(Posts, null=True, blank=True, related_name='interest_userpost')
    ip_tracker = models.ForeignKey(IpTracker, null=True, blank=True, related_name='interest_usertrack')
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' %(self.ip_tracker)


class ContactsViewed(models.Model):
    post_name = models.ForeignKey(Posts, null=True, blank=True, related_name='contact_userpost')
    ip_tracker = models.ForeignKey(IpTracker, null=True, blank=True, related_name='contact_usertrack')
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s'%(self.post_name)



class AboutUs(models.Model):
    site = models.OneToOneField(Site)
    banner = models.ImageField(upload_to='banners/')
    description = models.TextField(('Company Overview'))

    def __unicode__(self):
        return u'%s' % self.site


class OurTema(models.Model):
    avatar = models.ImageField(upload_to='images/')
    name = models.CharField(('Name'), max_length=150)
    title = models.CharField(('Title'), max_length=150)
    description = models.TextField('Description')
    testimonial = models.TextField(('Client Testimonial1'))

    def __unicode__(self):
        return self.name

class Testimonials(models.Model):
    name = models.CharField('Name', max_length=100)
    title = models.CharField('Title', max_length=100)
    avatar = models.ImageField('Avatar', upload_to='banners/')
    testimonial = models.TextField('Testimonial')

    def __unicode__(self):
        return self.name


class WebSiteContents(models.Model):
    site = models.OneToOneField(Site)
    signin = models.TextField('Signin', max_length=150)
    signup = models.TextField('Signup', max_length=150)

    def __unicode__(self):
        return u'%s' % self.site

class Contact(models.Model):
    site = models.OneToOneField(Site)
    phone = models.BigIntegerField(('Phone'))
    email1 = models.EmailField('Email1')
    email2 = models.EmailField('Email2')
    address = models.TextField('Address')
    skype = models.CharField(('Skype'), max_length=150)
    fb_link = models.CharField(('FB Link'), max_length=150)
    tw_link = models.CharField(('FB Link'), max_length=150)
    ln_link = models.CharField(('FB Link'), max_length=150)
    youtube_link = models.CharField(('FB Link'), max_length=150)
    googleplus_link = models.CharField(('FB Link'), max_length=150)


    def __unicode__(self):
        return u'%s' % self.site

