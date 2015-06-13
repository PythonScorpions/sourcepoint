from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, Context
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, UpdateView, DetailView
from apps.accounts.models import *
from apps.posts.forms import PostForm
from apps.posts.models import *
import json
from django.contrib.auth.decorators import login_required
from sourcepoint import settings


class Homepage(TemplateView):
    template_name = 'index.html'

    def keywords(self, *args, **kwargs):
        keywords = []
        for cat in Category.objects.all():
            keywords.append(str(cat.name))
        for tag in TechnologyTags.objects.all():
            keywords.append(str(tag.tag))
        return keywords

    def get_sellposts(self, *args, **kwargs):
        print self.request.user
        if str(self.request.user) == 'AnonymousUser':
            posts_sell = Posts.objects.filter(publish=True, sell_code=True).order_by('-created_dattetime')
        else:
            posts_sell = Posts.objects.filter(publish=True, sell_code=True).order_by('-created_dattetime').exclude(user=self.request.user)
        return posts_sell

    def get_buyposts(self, *args, **kwargs):
        if str(self.request.user) == 'AnonymousUser':
            posts_buy = Posts.objects.filter(publish=True, buy_code=True).order_by('-created_dattetime')
        else:
            posts_buy = Posts.objects.filter(publish=True, buy_code=True).order_by('-created_dattetime').exclude(user=self.request.user)
        return posts_buy

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        context['posts_sell'] = self.get_sellposts()
        context['sell'] = 'sell'
        context['buy'] = 'buy'
        context['posts_buy'] = self.get_buyposts()
        context['keywords'] = self.keywords()
        return context


class CategoryList(TemplateView):
    template_name = 'posts/category-posts.html'

    def get_posts(self,*args, **kwargs):
        type = self.kwargs['type']
        print "asasasas",Category.objects.get(slug=self.kwargs['category'])
        categories = Category.objects.get(slug=self.kwargs['category'])
        if type == 'sell':
            if str(self.request.user) == 'AnonymousUser':
                posts = Posts.objects.filter(category=categories,publish=True,sell_code=True)
            else:
                posts = Posts.objects.filter(category=categories,publish=True,sell_code=True).exclude(user=self.request.user)
        elif type == 'buy':
            if str(self.request.user) == 'AnonymousUser':
                posts = Posts.objects.filter(category=categories,publish=True,buy_code=True)
            else:
                posts = Posts.objects.filter(category=categories,publish=True,buy_code=True).exclude(user=self.request.user)
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not UserSubscriptions.objects.filter(user=self.request.user).exists():
            return redirect('/accounts/subscribe/?redirect=true&post=%s'%(kwargs['slug']))
        return super(PostDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['post'] = Posts.objects.get(slug=self.kwargs['slug'])
        if UserSubscriptions.objects.filter(user=self.request.user).exists():
            context['plan'] = UserSubscriptions.objects.get(user=self.request.user)
        try:
            context['tracker'] = IpTracker.objects.get(user=self.request.user)
        except:
            pass
        return context



def addpost(request):
    template_name = 'posts/post-your-requarment.html'
    form = PostForm
    tech_tags = TechnologyTags.objects.all()
    user = UserProfiles.objects.get(user=request.user)
    saved_tags = []
    tags = []
    data = TechnologyTags.objects.all()
    for d in data:
        tags.append(str(d.tag))
    obj = User.objects.get(username=request.user)
    if request.method == 'POST':
        type = request.POST.get('code')
        tags = request.POST.get('tags')
        print tags
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
            return redirect('/posts/preview/%s' % post.id)
        else:
            print "error", form.errors
    return render_to_response(template_name, {'form': form, 'user': user, 'tech_tags': tech_tags, 'tags':tags}, context_instance = RequestContext(request))

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
        user = UserProfiles.objects.get(user=request.user)
        form = self.form_class(instance=posts)
        return render_to_response(self.template_name, {'form': form, 'post': posts, 'user': user},
                                  context_instance=RequestContext(request),)

    def post(self, request, *args, **kwargs):
        posts = Posts.objects.get(id=kwargs['id'])
        form = self.form_class(request.POST, request.FILES, instance=posts)
        user = UserProfiles.objects.get(user=request.user)
        obj = User.objects.get(username=request.user)
        type = request.POST.get('code')
        tags = request.POST.get('tags')
        data = request.GET.get('redirect')
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
            for p in posts.tags.all():
                posts.tags.remove(p)
            for s in saved_tags:
                post.tags.add(s)
            posts.publish = True
            posts.save()
            messages.success(request, 'Posts Editted Successfully.')
            if data == 'true':
                return redirect('/posts/preview/%s/'%(posts.id))
            else:
                return redirect('/posts/preview/%s/'%(posts.id))
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
        context['contact_count'] = IpTracker.objects.filter(posts=Posts.objects.get(id=self.kwargs['id'])).count()
        context['interest_count'] = IpTracker.objects.filter(intersets=Posts.objects.get(id=self.kwargs['id'])).count()
        context['user_shown_interests'] = IpTracker.objects.filter(intersets=Posts.objects.get(id=self.kwargs['id']))
        return context

def postdelete(request,id):
    template_name = 'posts/my-posting.html'
    if Posts.objects.filter(id=id).exists():
        post = Posts.objects.get(id=id).delete()
        return redirect('/my-posting/')
        messages.success(request, 'Post Deleted Successfully')
    return render_to_response(template_name, context_instance=RequestContext(request))

class PostContact(TemplateView):
    template_name = 'posts/job-detail-contact-info.html'

    def get_client_ip(self,  *args, **kwargs):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


    def get(self, request, *args, **kwargs):
        plan = UserSubscriptions.objects.get(user=request.user)
        ip = self.get_client_ip()
        post = Posts.objects.get(slug=kwargs['slug'])
        tracker = ''
        try:
            tracker = IpTracker.objects.get(user=request.user)
            visted_posts = tracker.posts.all()
            if post in visted_posts:
                pass
            else:
                tracker.view_count +=1
                tracker.save()
                tracker.posts.add(post)
        except IpTracker.DoesNotExist:
            track = IpTracker()
            track.user = User.objects.get(id=request.user.id)
            track.ip = self.get_client_ip()
            track.view_count += 1
            track.save()
            track.posts.add(post)
        return render_to_response(self.template_name, {'post': post, 'tracker': tracker, 'plan': plan}, context_instance=RequestContext(request))

class SendContact(TemplateView):
    template_name = 'posts/job-detail-contact-info.html'

    def get_client_ip(self,  *args, **kwargs):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get(self, request, *args, **kwargs):
        ip = self.get_client_ip()
        post = Posts.objects.get(slug=kwargs['slug'])
        try:
            tracker = IpTracker.objects.get(user=request.user)

            if not tracker.intersets.filter(id=post.id).exists():
                tracker.interest_count += 1
                tracker.save()
                tracker.intersets.add(post)
        except IpTracker.DoesNotExist:
            track = IpTracker()
            track.user = User.objects.get(id=request.user.id)
            track.ip = self.get_client_ip()
            track.interest_count += 1
            track.save()
            track.intersets.add(post)
        site = Site.objects.get(pk=1)
        t = loader.get_template('posts/interest.txt')
        c = Context({'first_name': request.user.first_name, 'last_name': request.user.last_name,
                     'email': request.user.email, 'site': site.name, 'post_first_name': post.user.first_name,
                    'post_last_name': post.user.last_name})
        send_mail('[%s] %s' % (site.name, 'Interest Shown to Post'), t.render(c),
                  settings.DEFAULT_FROM_EMAIL, [post.user.email], fail_silently=False)
        return render_to_response(self.template_name, {'post':post}, context_instance=RequestContext(request))


class MyInterests(TemplateView):
    template_name = 'posts/my-interest.html'

    def get_interests(self, *args, **kwargs):
        interests = []
        interests1 = []
        posts_contacted = []
        interest_shown = []
        if IpTracker.objects.filter(user=self.request.user).exists():
            posts = IpTracker.objects.get(user=self.request.user)
            for p in posts.posts.all():
                posts_contacted.append(p)
            for i in posts.intersets.all():
                interest_shown.append(i)
            interests = posts_contacted + interest_shown
            final_posts = list(set(interests))
        else:
            final_posts = []
        return final_posts


    def get_context_data(self, **kwargs):
        context = super(MyInterests, self).get_context_data(**kwargs)
        print "sdsd",self.get_interests()
        context['final_posts'] = self.get_interests()
        return context

class MyInterestDetail(TemplateView):
    template_name = 'posts/my-interest-detail.html'

    def get_context_data(self, **kwargs):
        context = super(MyInterestDetail, self).get_context_data(**kwargs)
        context['post'] = Posts.objects.get(slug = self.kwargs['slug'])
        return context

def delete_interest(request, slug):
    template_name = 'posts/my-interest.html'
    if IpTracker.objects.filter(user=request.user).exists():
        tracker = IpTracker.objects.get(user=request.user)
        post = Posts.objects.get(slug=slug)
        obj = tracker.intersets.get(id=post.id)
        obj.delete()
        return redirect('/my-interests/')
    return render_to_response(template_name, context_instance=RequestContext(request))

class SearchResults(TemplateView):
    template_name = 'search.html'

    def keywords(self, *args, **kwargs):
        keywords = []
        for cat in Category.objects.all():
            keywords.append(str(cat.name))
        for tag in TechnologyTags.objects.all():
            keywords.append(str(tag.tag))
        return keywords

    def search_results(self, *args, **kwargs):
        results = []
        if 'search' in self.request.GET:
            try:
                if Category.objects.filter(name=self.request.GET.get('search')).exists():
                    category = Category.objects.get(name=self.request.GET.get('search'))
                    results = Posts.objects.filter(category=category)
                elif TechnologyTags.objects.filter(tag=self.request.GET.get('search')).exists():
                    tags = TechnologyTags.objects.get(tag=self.request.GET.get('search'))
                    results = Posts.objects.filter(tags=tags)
            except:
                pass
        else:
            pass
        return results

    def get_context_data(self, **kwargs):
        context = super(SearchResults, self).get_context_data(**kwargs)
        context['posts_sell'] = Posts.objects.filter(publish=True, sell_code=True).order_by('-created_date')
        context['sell'] = 'sell'
        context['buy'] = 'buy'
        context['posts_buy'] = Posts.objects.filter(publish=True, buy_code=True).order_by('-created_date')
        context['keywords'] = self.keywords()
        context['results'] = self.search_results()
        return context












