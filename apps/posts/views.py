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
from apps.posts.forms import PostForm, PostPreviewForm
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
        posts_sell = Posts.objects.filter(publish=True, sell_code=True).order_by('-created_dattetime')
        return posts_sell

    def get_buyposts(self, *args, **kwargs):
        posts_buy = Posts.objects.filter(publish=True, buy_code=True).order_by('-created_dattetime')
        return posts_buy

    def deactivate_post(self):
        try:
            tracker = IpTracker.objects.get(user=self.request.user)
            plan = UserSubscriptions.objects.get(user=self.request.user)
            if tracker.post_count == plan.plan.post_requirement:
                post = 'deactivate'
            else:
                post = ''
        except:
            post = ''
        return post

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        context['posts_sell'] = self.get_sellposts()
        context['sell'] = 'sell'
        context['buy'] = 'buy'
        context['posts_buy'] = self.get_buyposts()
        context['keywords'] = self.keywords()
        context['post_activate'] = self.deactivate_post()
        return context


class CategoryList(TemplateView):
    template_name = 'posts/category-posts.html'

    def get_posts(self,*args, **kwargs):
        type = self.kwargs['type']
        if not self.kwargs['category'] == 'other':
            categories = Category.objects.get(slug=self.kwargs['category'])
        if not self.kwargs['category'] == 'other':
            if type == 'sell':
                if str(self.request.user) == 'AnonymousUser':
                    posts = Posts.objects.filter(category=categories,publish=True, sell_code=True).order_by('-created_dattetime')
                else:
                    posts = Posts.objects.filter(category=categories,publish=True, sell_code=True).order_by('-created_dattetime')
            elif type == 'buy':
                if str(self.request.user) == 'AnonymousUser':
                    posts = Posts.objects.filter(category=categories,publish=True,buy_code=True).order_by('-created_dattetime')
                else:
                    posts = Posts.objects.filter(category=categories,publish=True,buy_code=True).order_by('-created_dattetime')
            else:
                posts = ''
        else:
            categories = Category.objects.all()[:3]
            if type == 'sell':
                posts = Posts.objects.filter(publish=True,sell_code=True).order_by('-created_dattetime').exclude(category__name__in=[c.name for c in categories])
            elif type == 'buy':
                posts = Posts.objects.filter(publish=True,buy_code=True).order_by('-created_dattetime').exclude(category__name__in=[c.name for c in categories])
            else:
                pass
        return posts

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['posts'] = self.get_posts()
        context['sell'] = 'sell'
        context['buy'] = 'buy'
        context['selected_cat'] = self.kwargs['category']
        context['type'] = self.kwargs['type']
        if self.kwargs['category'] == 'other':
            context['cat_other'] = 'other'
        return context


class PostDetail(TemplateView):
    template_name = 'posts/job-detail-after-login.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['post'] = Posts.objects.get(slug=self.kwargs['slug'])
        try:
            if UserSubscriptions.objects.filter(user=self.request.user).exists():
                context['plan'] = UserSubscriptions.objects.get(user=self.request.user)
            try:
                context['tracker'] = IpTracker.objects.get(user=self.request.user)
            except:
                pass
            # try:
            post = Posts.objects.get(slug=self.kwargs['slug'])
            try:
                ip_tracker = IpTracker.objects.get(user=self.request.user)
                if InterestOfUsers.objects.filter(post_name=post).exists():
                    context['interest'] = 'true'
                if post in ip_tracker.posts.all():
                    context['contact'] = 'true'
            except:
                pass
        except:
            pass
        return context


    # trackers = IpTracker.objects.get(user=request.user)
    #
    #         if not trackers.intersets.filter(id=post.id).exists():
    #             post_obj = Posts.objects.get(slug=kwargs['slug'])
    #             if not InterestOfUsers.objects.filter(post_name=post_obj, ip_tracker=trackers).exists():
    #                 trackers.interest_count += 1
    #                 trackers.save()
    #                 trackers_obj = IpTracker.objects.get(user=request.user)



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
        form1 = PostPreviewForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(user=obj, type=type)
            post_preview = form1.save(user=obj, type=type, post=post)
            for s in saved_tags:
                post.tags.add(s)
                post_preview.tags.add(s)
            if IpTracker.objects.filter(user=request.user).exists():
                tracker = IpTracker.objects.get(user=request.user)
                tracker.post_count += 1
                tracker.save()
            else:
                tracker = IpTracker()
                tracker.user = User.objects.get(username=request.user)
                tracker.post_count +=1
                tracker.save()
            return redirect('/posts/preview/%s' % post_preview.id)
        else:
            print "error", form.errors
    return render_to_response(template_name, {'form': form, 'user': user, 'tech_tags': tech_tags, 'tags':tags}, context_instance = RequestContext(request))

class Preview(TemplateView):
    template_name = 'posts/my-posting-detail.html'

    def get_tags(self,  *args, **kwargs):
        posts = PostsPreview.objects.get(id=self.kwargs['id'])
        tags = posts.tags.all()
        return tags

    def get_context_data(self, **kwargs):
        context = super(Preview, self).get_context_data(**kwargs)
        context['post'] = PostsPreview.objects.get(id=kwargs['id'])
        context['user'] = UserProfiles.objects.get(user=self.request.user)
        context['tags'] = self.get_tags()
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('publish'):
            posts = PostsPreview.objects.get(id=kwargs['id'])
            posts.preview.title = posts.title
            posts.preview.description = posts.description
            posts.preview.category = posts.category
            posts.preview.prices = posts.prices
            posts.preview.sell_code = posts.sell_code
            posts.preview.buy_code = posts.buy_code
            posts.preview.mobile = posts.mobile
            posts.preview.file = posts.file
            posts.preview.skypeid = posts.skypeid
            posts.preview.email = posts.email
            posts.preview.publish = posts.publish
            for s in posts.preview.tags.all():
                posts.preview.tags.remove(s)
            for p in posts.tags.all():
                posts.preview.tags.add(p)
            posts.preview.publish = True
            posts.preview.save()
            PostsPreview.objects.get(id=kwargs['id']).delete()
            return redirect('/')
        return render_to_response(self.template_name, context_instance = RequestContext(request))

class PostEdit(UpdateView):
    template_name = 'posts/update-post.html'
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        if PostsPreview.objects.filter(id=kwargs['id']).exists():
            posts = PostsPreview.objects.get(id=kwargs['id'])
            user = UserProfiles.objects.get(user=request.user)
            form = PostPreviewForm(instance=posts)
        else:
            posts = Posts.objects.get(id=kwargs['id'])
            user = UserProfiles.objects.get(user=request.user)
            form = self.form_class(instance=posts)
        return render_to_response(self.template_name, {'form': form, 'post': posts, 'user': user},
                                  context_instance=RequestContext(request),)

    def post(self, request, *args, **kwargs):
        if PostsPreview.objects.filter(id=kwargs['id']).exists():
            preview = PostsPreview.objects.get(id=kwargs['id'])
            posts = preview.preview
            form1 = PostPreviewForm(request.POST, request.FILES, instance=preview)
            form = self.form_class(request.POST, request.FILES, instance=posts)
        else:
            posts = Posts.objects.get(id=kwargs['id'])
            form1 = PostPreviewForm(request.POST, request.FILES)
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
            post = form1.save(user=obj, type=type, post=posts)
            for p in posts.tags.all():
                post.tags.remove(p)
            for s in saved_tags:
                post.tags.add(s)
            if data == 'true':
                return redirect('/posts/preview/%s/'%(post.id))
            else:
                return redirect('/posts/preview/%s/'%(post.id))
        else:
            print "errors",form.errors
        return render_to_response(self.template_name, {'form': form1, 'id': id}, context_instance=RequestContext(request))


class MyPosting(TemplateView):
    template_name = 'posts/my-posting.html'

    def get_context_data(self, **kwargs):
        context = super(MyPosting, self).get_context_data(**kwargs)
        context['posts_buy'] = Posts.objects.filter(user=self.request.user, buy_code=True).order_by('-created_dattetime')
        context['posts_sell'] = Posts.objects.filter(user=self.request.user, sell_code=True).order_by('-created_dattetime')
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
    template_name = 'posts/job-detail-get-contact.html'

    def get_client_ip(self,  *args, **kwargs):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


    def get(self, request, *args, **kwargs):
        interest = ''
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
                if not ContactsViewed.objects.filter(post_name=post, ip_tracker=tracker).exists():
                    tracker.view_count +=1
                    tracker.save()
                    tracker.posts.add(post)
                    ContactsViewed.objects.create(post_name=post, ip_tracker=tracker)
        except IpTracker.DoesNotExist:
            track = IpTracker()
            track.user = User.objects.get(id=request.user.id)
            track.ip = self.get_client_ip()
            track.view_count += 1
            track.save()
            track.posts.add(post)
            ContactsViewed.objects.create(post_name=post, ip_tracker=track)
        ip_tracker = IpTracker.objects.get(user=self.request.user)
        if InterestOfUsers.objects.filter(post_name=post).exists():
            interest = 'true'

        return render_to_response(self.template_name, {'post': post, 'tracker': tracker, 'plan': plan,
                                                       'interest': interest,},
                                  context_instance=RequestContext(request))

    # if not InterestOfUsers.objects.filter(post_name=post_obj, ip_tracker=trackers).exists():
    #                 trackers.interest_count += 1
    #                 trackers.save()
    #                 trackers_obj = IpTracker.objects.get(user=request.user)
    #
    #                 InterestOfUsers.objects.create(post_name=post_obj, ip_tracker=trackers_obj)


    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['post'] = Posts.objects.get(slug=self.kwargs['slug'])
        if UserSubscriptions.objects.filter(user=self.request.user).exists():
            context['plan'] = UserSubscriptions.objects.get(user=self.request.user)
        try:
            context['tracker'] = IpTracker.objects.get(user=self.request.user)
        except:
            pass
        # try:
        post = Posts.objects.get(slug=self.kwargs['slug'])
        try:
            ip_tracker = IpTracker.objects.get(user=self.request.user)
            if post in ip_tracker.intersets.all():
                context['interest'] = 'true'
            if post in ip_tracker.posts.all():
                context['contact'] = 'true'
        except:
            pass
        return context

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
        plan = UserSubscriptions.objects.get(user=request.user)
        interest = ''
        contact = ''
        try:
            trackers = IpTracker.objects.get(user=request.user)

            if not trackers.intersets.filter(id=post.id).exists():
                post_obj = Posts.objects.get(slug=kwargs['slug'])
                if not InterestOfUsers.objects.filter(post_name=post_obj, ip_tracker=trackers).exists():
                    trackers.interest_count += 1
                    trackers.save()
                    trackers_obj = IpTracker.objects.get(user=request.user)

                    InterestOfUsers.objects.create(post_name=post_obj, ip_tracker=trackers_obj)
        except IpTracker.DoesNotExist:
            post_obj = Posts.objects.get(slug=kwargs['slug'])
            track = IpTracker()
            track.user = User.objects.get(id=request.user.id)
            track.ip = self.get_client_ip()
            track.interest_count += 1
            track.save()
            InterestOfUsers.objects.create(post_name=post_obj, ip_tracker=track)
        site = Site.objects.get(pk=1)
        ip_tracker = IpTracker.objects.get(user=self.request.user)
        if InterestOfUsers.objects.filter(post_name=post).exists():
            interest = 'true'
        if post in ip_tracker.posts.all():
            contact = 'true'

        t = loader.get_template('posts/interest.txt')
        c = Context({'first_name': request.user.first_name, 'last_name': request.user.last_name,
                     'email': request.user.email, 'site': site.name, 'post_first_name': post.user.first_name,
                    'post_last_name': post.user.last_name})
        send_mail('[%s] %s' % (site.name, 'Interest Shown to Post'), t.render(c),
                  settings.DEFAULT_FROM_EMAIL, [post.user.email], fail_silently=False)

        return render_to_response(self.template_name, {'post': post, 'interest': interest, 'contact': contact,
                                                       'plan': plan}, context_instance=RequestContext(request))


class MyInterests(TemplateView):
    template_name = 'posts/my-interest.html'


    def buy_posts(self, *args, **kwargs):
        contact_buy_post = []
        interest_buy_post = []
        posts_contacted = []
        interest_shown = []

        if IpTracker.objects.filter(user=self.request.user).exists():
            posts = IpTracker.objects.get(user=self.request.user)
            for p in posts.posts.all():
                if p.buy_code == True:
                    if ContactsViewed.objects.filter(ip_tracker_id=posts.id).exists():
                        interest_buy_code = ContactsViewed.objects.filter(ip_tracker=posts, post_name__buy_code=True).order_by('-date')
                        for i in interest_buy_code:
                            posts_shown = Posts.objects.filter(title=i.post_name.title)
                            posts_contacted.append(posts_shown)
                            for p in posts_shown:
                                contact_buy_post.append(p)
            if InterestOfUsers.objects.filter(ip_tracker_id=posts.id).exists():
                interest_buy_post = InterestOfUsers.objects.filter(ip_tracker=posts, post_name__buy_code=True).order_by('-date')
                for i in interest_buy_post:
                    posts_shown = Posts.objects.filter(title=i.post_name.title)
                    for p in posts_shown:
                        interest_shown.append(p)
            code_buy = contact_buy_post +interest_shown
            code_buy = list(set(code_buy))
        else:
            code_buy = []
        final_post = Posts.objects.filter(title__in=[c for c in code_buy], buy_code=True).order_by('-created_dattetime')
        return final_post

    def sell_posts(self, *args, **kwargs):
        contact_sell_post = []
        interest_shown = []
        if IpTracker.objects.filter(user=self.request.user).exists():
            posts = IpTracker.objects.get(user=self.request.user)
            for p in posts.posts.all():
                if p.sell_code == True:
                    if ContactsViewed.objects.filter(ip_tracker_id=posts.id).exists():
                        interest_sell_code = ContactsViewed.objects.filter(ip_tracker=posts, post_name__sell_code=True).order_by('-date')
                        for i in interest_sell_code:
                            posts_shown = Posts.objects.filter(title=i.post_name.title)
                            for p in posts_shown:
                                contact_sell_post.append(p)

            if InterestOfUsers.objects.filter(ip_tracker_id=posts.id).exists():
                interest_sell_code = InterestOfUsers.objects.filter(ip_tracker=posts, post_name__sell_code=True).order_by('-date')
                for i in interest_sell_code:
                    posts_data = Posts.objects.filter(title=i.post_name.title)
                    for p in posts_data:
                        interest_shown.append(p)

            code_sell = contact_sell_post + interest_shown
            code_sell = list(set(code_sell))
        else:
            code_sell = []
        final_post = Posts.objects.filter(title__in=[c for c in code_sell],sell_code=True).order_by('-created_dattetime')

        return final_post


    def get_context_data(self, **kwargs):
        context = super(MyInterests, self).get_context_data(**kwargs)
        # context['final_posts'] = self.get_interests()
        context['buy_posts'] = self.buy_posts()
        context['sell_posts'] = self.sell_posts()
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
        if InterestOfUsers.objects.filter(ip_tracker=tracker, post_name=post).exists():
            interests = InterestOfUsers.objects.get(ip_tracker=tracker, post_name=post)
            interests.delete()
        for t in tracker.posts.all():
            if t == post:
                tracker.posts.remove(t)
                if ContactsViewed.objects.filter(ip_tracker=tracker, post_name=post).exists():
                    interests = ContactsViewed.objects.get(ip_tracker=tracker, post_name=post)
                    interests.delete()
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


class PostsBuy(TemplateView):
    template_name = 'posts/posts-buy.html'

    def keywords(self, *args, **kwargs):
        keywords = []
        for cat in Category.objects.all():
            keywords.append(str(cat.name))
        for tag in TechnologyTags.objects.all():
            keywords.append(str(tag.tag))
        return keywords

    def get_sellposts(self, *args, **kwargs):
        posts_sell = Posts.objects.filter(publish=True, sell_code=True).order_by('-created_dattetime')
        return posts_sell

    def get_buyposts(self, *args, **kwargs):
        posts_buy = Posts.objects.filter(publish=True, buy_code=True).order_by('-created_dattetime')
        return posts_buy

    def deactivate_post(self):
        try:
            tracker = IpTracker.objects.get(user=self.request.user)
            plan = UserSubscriptions.objects.get(user=self.request.user)
            if tracker.post_count == plan.plan.post_requirement:
                post = 'deactivate'
            else:
                post = ''
        except:
            post = ''
        return post

    def get_context_data(self, **kwargs):
        context = super(PostsBuy, self).get_context_data(**kwargs)
        context['posts_sell'] = self.get_sellposts()
        context['sell'] = 'sell'
        context['buy'] = 'buy'
        context['posts_buy'] = self.get_buyposts()
        context['keywords'] = self.keywords()
        context['post_activate'] = self.deactivate_post()
        return context













