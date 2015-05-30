from django.contrib import messages
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import TemplateView, FormView, UpdateView, DetailView
from apps.accounts.models import *
from apps.posts.forms import PostForm
from apps.posts.models import *


class Homepage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        context['posts_sell'] = Posts.objects.filter(publish=True, sell_code=True).order_by('-created_date')
        context['sell'] = 'sell'
        context['buy'] = 'buy'
        context['posts_buy'] = Posts.objects.filter(publish=True, buy_code=True).order_by('-created_date')
        return context


class CategoryList(TemplateView):
    template_name = 'posts/category-posts.html'

    def get_posts(self,*args, **kwargs):
        type = self.kwargs['type']
        print "asasasas",Category.objects.get(slug=self.kwargs['category'])
        categories = Category.objects.get(slug=self.kwargs['category'])
        if type == 'sell':
            posts = Posts.objects.filter(category=categories,publish=True,sell_code=True)
        elif type == 'buy':
            posts = Posts.objects.filter(category=categories,publish=True,buy_code=True)
        else:
            posts = ''
        return posts

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['posts'] = self.get_posts()
        context['sell'] = 'sell'
        context['buy'] = 'buy'
        context['selected_cat'] = self.kwargs['category']
        context['type'] = self.kwargs['type']
        return context

class PostDetail(TemplateView):
    template_name = 'posts/job-detail-after-login.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['post'] = Posts.objects.get(id=self.kwargs['id'])
        return context



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

    def post(self, request, *args ,**kwargs):
        if request.POST.get('publish'):
            posts = Posts.objects.get(id=kwargs['id'])
            posts.publish = True
            posts.save()
            return redirect('/')
        return render_to_response(self.template_name, context_instance = RequestContext(request))

class PostEdit(UpdateView):
    template_name = 'posts/update-post.html'
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        posts = Posts.objects.get(id=kwargs['id'])
        form = self.form_class(instance = posts)
        return render_to_response(self.template_name, {'form': form, 'post': posts}, context_instance=RequestContext(request),)

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
            posts.publish = True
            posts.save()
            messages.success(request, 'Posts Editted Successfully.')
            return redirect('/')
        else:
            print "errors",form.errors
        return render_to_response(self.template_name, {'form': form, 'id': id}, context_instance=RequestContext(request))


class MyPosting(TemplateView):
    template_name = 'posts/my-posting.html'

    def get_context_data(self, **kwargs):
        context = super(MyPosting, self).get_context_data(**kwargs)
        context['posts_buy'] = Posts.objects.filter(user=self.request.user, buy_code=True)
        context['posts_sell'] = Posts.objects.filter(user=self.request.user, sell_code=True)
        context['today_date'] = datetime.datetime.now().date()
        return context

class MyPostDetail(TemplateView):
    template_name = 'posts/post-detail.html'

    def get_context_data(self, **kwargs):
        context = super(MyPostDetail, self).get_context_data(**kwargs)
        context['post'] = Posts.objects.get(id=self.kwargs['id'])
        context['user'] = UserProfiles.objects.get(user=self.request.user)
        return context

def postdelete(request,id):
    template_name = 'posts/my-posting.html'
    if Posts.objects.filter(id=id).exists():
        post = Posts.objects.get(id=id).delete()
        return redirect('/my-posting/')
        messages.success(request, 'Post Deleted Successfully')
    return render_to_response(template_name, context_instance=RequestContext(request))



