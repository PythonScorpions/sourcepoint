from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView, FormView
from apps.accounts.forms import RegisterForm
from apps.accounts.models import *
from apps.posts.forms import PostForm
from apps.posts.models import *


class Homepage(TemplateView):
    template_name = 'index.html'


def addpost(request):
    template_name = 'posts/post-your-requarment.html'
    form = PostForm
    tech_tags = TechnologyTags.objects.all()
    user = UserProfiles.objects.get(user=request.user)
    saved_tags = []
    obj = User.objects.get(username=request.user)
    if request.method == 'POST':
        type = request.POST.get('code')
        tags = request.POST.get('tags')
        split_tags = tags.split(',')
        for t in split_tags:
            if TechnologyTags.objects.filter(tag=t).exists():
                tag = TechnologyTags.objects.get(tag=t)
                saved_tags.append(tag)
            else:
                tag = TechnologyTags.objects.create(tag=t)
                saved_tags.append(tag)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(user=obj, type=type)
            for s in saved_tags:
                post.tags.add(s)
            messages.success(request, 'Post Successfully Submitted')
        else:
            print "error", form.errors
    return render_to_response(template_name, {'form': form, 'user': user, 'tech_tags': tech_tags}, context_instance = RequestContext(request))

