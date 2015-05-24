from apps.posts.models import *
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'user', 'category')
    # list_editable = ('mobile','email',)
    filter_horizontal = ('tags',)

admin.site.register(Posts, PostAdmin)
admin.site.register(Category)
admin.site.register(TechnologyTags)