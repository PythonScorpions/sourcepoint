from django.contrib import messages
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import TemplateView, FormView, UpdateView
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
            return redirect('/posts/preview/%s' % post.id)
        else:
            print "error", form.errors
    return render_to_response(template_name, {'form': form, 'user': user, 'tech_tags': tech_tags}, context_instance = RequestContext(request))

class Preview(TemplateView):
    template_name = 'posts/my-posting-detail.html'

    def get_tags(self,  *args, **kwargs):
        posts = Posts.objects.get(id=self.kwargs['id'])
        tags = posts.tags.all()
        return tags

    def get_context_data(self, **kwargs):
        context = super(Preview, self).get_context_data(**kwargs)
        context['post'] = Posts.objects.get(id=kwargs['id'])
        context['user'] = UserProfiles.objects.get(user=self.request.user)
        context['tags'] = self.get_tags()
        return context

class PostEdit(UpdateView):
    template_name = 'posts/update-post.html'
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        posts = Posts.objects.get(id=kwargs['id'])
        form = self.form_class(instance = posts)
        return render_to_response(self.template_name, {'form': form, 'post':posts}, context_instance=RequestContext(request),)

    def post(self, request, *args, **kwargs):
        posts = Posts.objects.get(id=kwargs['id'])
        form = self.form_class(request.POST, request.FILES, instance=posts)
        user = UserProfiles.objects.get(user=request.user)
        obj = User.objects.get(username=request.user)
        type = request.POST.get('code')
        tags = request.POST.get('tags')
        split_tags = tags.split(',')
        saved_tags = []
        for t in split_tags:
            if TechnologyTags.objects.filter(tag=t).exists():
                tag = TechnologyTags.objects.get(tag=t)
                saved_tags.append(tag)
            else:
                tag = TechnologyTags.objects.create(tag=t)
                saved_tags.append(tag)
        if form.is_valid():
            post = form.save(user=obj, type=type)
            for s in saved_tags:
                post.tags.add(s)
            messages.success(request, 'Posts Editted Successfully.')
            return redirect('/post-edit/21/')
        else:
            print "errors",form.errors
        return render_to_response(self.template_name, {'form': form, 'id': id}, context_instance=RequestContext(request))

