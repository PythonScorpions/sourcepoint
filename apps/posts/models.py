from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField

class Category(models.Model):
    name = models.CharField('Category',max_length=100)
    slug = AutoSlugField(populate_from='name')

    def __unicode__(self):
        return self.name

class TechnologyTags(models.Model):
    tag = models.CharField('Tag',max_length=150)

    def __unicode__(self):
        return self.tag

class Posts(models.Model):

    PRICES = (
        ('1', '< $10'),
        ('2', '$10 to $50'),
        ('3', '$50 to $100'),
        ('4', '$100 to 200'),
        ('5', '$200 to $300'),
        ('6', '$300 to $500'),
        ('7', '$500 to $750'),
        ('8', '$750 to $1000'),
        ('9', '$1000 to $5000'),
        ('10', 'Not Fixed')
    )

    user = models.ForeignKey(User, related_name='user_posts')
    category = models.ForeignKey(Category)
    title = models.CharField('Post Title',max_length=150)
    description = models.TextField('Description')
    file = models.FileField('File',upload_to='files/', null=True, blank=True)
    mobile = models.BooleanField('Hide Mobile', default=False)
    skypeid = models.BooleanField('SkypeId', default=False)
    prices = models.CharField('Prices',choices=PRICES,max_length=150)
    email = models.BooleanField('Hide Email', default=False)
    tags = models.ManyToManyField(TechnologyTags,null=True,blank=True)
    created_date = models.DateField('Created Date',auto_now=True)
    created_dattetime = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from='title')
    expiry_date = models.DateField('Expiry Date',null=True,blank=True)
    sell_code = models.BooleanField(default=False)
    buy_code = models.BooleanField(default=False)
    publish = models.BooleanField(default=False)
    user_contacted = models.ManyToManyField(User, null=True, blank=True)


    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class PostsPreview(models.Model):

    PRICES = (
        ('1', '< $10'),
        ('2', '$10 to $50'),
        ('3', '$50 to $100'),
        ('4', '$100 to 200'),
        ('5', '$200 to $300'),
        ('6', '$300 to $500'),
        ('7', '$500 to $750'),
        ('8', '$750 to $1000'),
        ('9', '$1000 to $5000'),
        ('10', 'Not Fixed')
    )

    user = models.ForeignKey(User, related_name='preview_posts')
    category = models.ForeignKey(Category)
    title = models.CharField('Post Title',max_length=150)
    description = models.TextField('Description')
    file = models.FileField('File',upload_to='files/', null=True, blank=True)
    mobile = models.BooleanField('Hide Mobile', default=False)
    skypeid = models.BooleanField('SkypeId', default=False)
    prices = models.CharField('Prices',choices=PRICES,max_length=150)
    email = models.BooleanField('Hide Email', default=False)
    tags = models.ManyToManyField(TechnologyTags,null=True,blank=True)
    created_date = models.DateField('Created Date',auto_now=True)
    created_dattetime = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from='title')
    expiry_date = models.DateField('Expiry Date',null=True,blank=True)
    sell_code = models.BooleanField(default=False)
    buy_code = models.BooleanField(default=False)
    publish = models.BooleanField(default=False)
    user_contacted = models.ManyToManyField(User, null=True, blank=True)
    preview = models.ForeignKey(Posts, null=True, blank=True, related_name='post_preview')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Post Preview'
        verbose_name_plural = 'Post Previews'

class UserInterests(models.Model):
    posts = models.OneToOneField(User, related_name= 'user_interests')
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return u'%s' % self.posts