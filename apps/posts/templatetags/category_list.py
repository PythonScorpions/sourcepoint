from django import template
from apps.posts.models import *

register = template.Library()

@register.assignment_tag()
def list_category():
    categories = Category.objects.all()[:3]
    return categories