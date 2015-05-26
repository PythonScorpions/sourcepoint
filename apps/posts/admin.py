from apps.posts.models import *
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'user', 'category','publish',)
    filter_horizontal = ('tags',)
    list_editable = ('publish', )

admin.site.register(Posts, PostAdmin)
admin.site.register(Category)
admin.site.register(TechnologyTags)