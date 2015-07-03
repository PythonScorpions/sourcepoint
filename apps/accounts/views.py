from random import randint
from billing import CreditCard, get_gateway
from billing.forms.stripe_forms import StripeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, QueryDict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, UpdateView
from django.views.generic import View
from django.template import loader
from django_extensions.db.fields import json
import json
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.forms import PayPalIPNForm
from paypal.standard.ipn.models import PayPalIPN
from apps.accounts.forms import *
from django.template import RequestContext, Context
from django.shortcuts import render_to_response, redirect, render
from django.contrib import messages
from sourcepoint import settings


class Loginpage(TemplateView):

    template_name = 'accounts/login.html'

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            # message = ''
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.success(request, "Your account is not activated yet, please check your email")
            else:
                messages.success(request, "Invalid Email or Password")
        return render_to_response(self.template_name, context_instance=RequestContext(request),)


def register(request):
    template_name = 'accounts/sign-up.html'
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            token = user.token
            t = loader.get_template('accounts/verify.txt')
            site = Site.objects.get(pk=1)
            # c = Context({'name': user.user.first_name, 'email':user.user.email, 'site': site.name, 'token': user.token})
            # send_mail('[%s] %s' % (site.name, 'New User Registration'), t.render(c), settings.DEFAULT_FROM_EMAIL, [user.user.email], fail_silently=False)
            # messages.success(request, 'Verificatioin link has send to your mail link has sent to your email')
            email = request.POST['email']
            password = request.POST['password2']
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/accounts/verification/%s/' % token)
                    messages.success(request, 'OTP has send to number')
        else:
            print "errors", form.errors
    return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request),)

def mail_sent(request):
    template_name= 'accounts/my-profile.html'
    t = loader.get_template('accounts/verify.txt')
    user = UserProfiles.objects.get(user=request.user)
    site = Site.objects.get(pk=1)
    c = Context({'name': user.user.first_name, 'email':user.user.email, 'site': site.name, 'token': user.token})
    send_mail('[%s] %s' % (site.name, 'New User Registration'), t.render(c), settings.DEFAULT_FROM_EMAIL, [user.user.email], fail_silently=False)
    messages.success(request, 'Verificatioin link has send to your mail link has sent to your email')
    return redirect('/accounts/update-profile/')
    return render_to_response(template_name, context_instance=RequestContext(request),)


def subscribe(request):
     template_name = 'accounts/pricing-plan.html'
     url = ''
     plans = SubscriptionPlan.objects.all()
     if 'redirect' in request.GET and request.GET['redirect'] == 'true':
         request.session['post'] = request.GET['post']
     if 'profile' in request.GET and request.GET['profile'] == 'true':
         request.session['url'] = '/accounts/update-profile/'

     if request.method == 'POST':
        if 'post' in request.session:
            post = request.session['post']
            del request.session['post']
            plan = SubscriptionPlan.objects.get(id=request.POST['plan'])
            subscribe = UserSubscriptions()
            profile = UserProfiles.objects.get(user=request.user)
            subscribe.user = profile.user
            subscribe.plan = plan
            subscribe.expiry_date = datetime.datetime.now()
            subscribe.save()
            request.session['price'] = subscribe.price
            return redirect('/post-detail/%s'%(post))
        elif 'url' in request.session:
            url = request.session['url']
            del request.session['url']
            plan = SubscriptionPlan.objects.get(id=request.POST['plan'])
            subscribe = UserSubscriptions()
            profile = UserProfiles.objects.get(user=request.user)
            subscribe.user = profile.user
            subscribe.plan = plan
            subscribe.expiry_date = datetime.datetime.now()
            subscribe.save()
            return redirect(url)
        else:
            plan = SubscriptionPlan.objects.get(id=request.POST['plan'])
            subscribe = UserSubscriptions()
            profile = UserProfiles.objects.get(user=request.user)
            subscribe.user = profile.user
            subscribe.plan = plan
            subscribe.expiry_date = datetime.datetime.now()
            subscribe.save()
            t = loader.get_template('accounts/verify.txt')
            site = Site.objects.get(pk=1)
            c = Context({'name': profile.user.first_name, 'email':profile.user.email, 'site': site.name, 'token': profile.token})
            send_mail('[%s] %s' % (site.name, 'New User Registration'), t.render(c), settings.DEFAULT_FROM_EMAIL, [profile.user.email], fail_silently=False)
            messages.success(request, 'Verificatioin link has send to your mail link has sent to your email')
            if plan.free_plan == True:
                return redirect('/accounts/thanku/?type=free')
            else:
                return redirect('/accounts/thanku/?type=paid')

     return render_to_response(template_name, {'plans': plans}, context_instance=RequestContext(request),)

class Verification(TemplateView):
    template_name = 'accounts/enter-otp.html'

    def post(self, request, *args, **kwargs):
        if UserProfiles.objects.filter(token=kwargs['key']).exists():
            user = UserProfiles.objects.get(token=kwargs['key'])
            user.user.is_active = True
            user.user.save()
            return redirect('/accounts/subscribe/')
        return render_to_response(self.template_name, context_instance=RequestContext(request),)

class EmailVerification(TemplateView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        token = kwargs['key']
        success = ''
        if UserProfiles.objects.filter(token=token).exists():
            user = UserProfiles.objects.get(token=token)
            user.email_verify = True
            user.save()
            success = 'Email has been Verified,Please Login'
            return redirect('/accounts/login/')
        return render_to_response(self.template_name,{'success': success},context_instance=RequestContext(request),)

def email_verification(request, key):
    template_name = 'accounts/login.html'
    if UserProfiles.objects.filter(token=key).exists():
        user = UserProfiles.objects.get(token=key)
        if user:
            user.email_verify = True
            user.save()
            if not request.user.is_authenticated():
                messages.success(request, 'Please Login')
                return redirect('/accounts/login/')
            else:
                return redirect('/accounts/update-profile/')
    else:
        messages.success(request, 'This Link is Expired')
        return redirect('/')
    return render_to_response(template_name, context_instance=RequestContext(request),)

class Thankyou(TemplateView):

    template_name = 'accounts/thank-you.html'

    def get(self, request, *args, **kwargs):
        plan = UserSubscriptions.objects.get(user=request.user)
        paypal_dict = \
            {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": plan.plan.price,
            "item_name": 'Plan Purchase',
            "invoice": int(randint(100,999)),
            "notify_url": "http://192.168.1.5:8000" + reverse('paypal-ipn'),
            "return_url": "http://192.168.1.5:8000/accounts/update-profile/",
            "cancel_return": "http://192.168.1.5:8000",

            }
        # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form}
        # form1 = CreditCardForm()
        # context = {"form": form,"course":course,"form1":form1,'name':name,'discount':discount,'message':message}
        return render(request,"accounts/thank-you.html", context)


    # def post(self, request, *args, **kwargs):
    #     paypal_dict = {
    #     "business": settings.PAYPAL_RECEIVER_EMAIL,
    #     "amount": 10,
    #     "cmd":'_xclick-subscriptions',
    #     "item_name": 'Test',
    #     "invoice": 111,
    #     "notify_url": "https://192.168.1.5:8000" + reverse('paypal-ipn'),
    #     "return_url": "192.168.1.5:8000",
    #     "cancel_return": "http://192.168.1.5:8000" ,
    #
    # }
    #     # Create the instance.
    #     form = PayPalPaymentsForm(initial=paypal_dict)
    #     context = {"form": form}
    #     # form1 = CreditCardForm()
    #     # context = {"form": form,"course":course,"form1":form1,'name':name,'discount':discount,'message':message}
    #     return render(request,"accounts/thank-you.html", context)

def user_logout(request):
    logout(request)
    return redirect('/')

class ForegetPassword(TemplateView):

    template_name = 'accounts/forgot-password.html'

    def post(self, request, *args, **kwargs):
        if User.objects.filter(email=request.POST['email']).exists():
            email = User.objects.get(email=request.POST['email'])
            user = UserProfiles.objects.get(user=email)
            site = Site.objects.get(pk=1)
            t = loader.get_template('accounts/password.txt')
            c = Context({'name': email.first_name, 'email':email, 'site': site.name, 'token': user.token})
            send_mail('[%s] %s' % (site.name, 'New Contactus Request'), t.render(c), settings.DEFAULT_FROM_EMAIL, [email.email], fail_silently=False)
            messages.success(request, 'Reset link has sent to your email')

        else:
            messages.success(request, 'User with this email Doesnt exist')
        return render_to_response(self.template_name, context_instance=RequestContext(request),)

class ResetPassword(TemplateView):

    template_name = 'accounts/change-password.html'

    def post(self, request, *args, **kwargs):
        user = UserProfiles.objects.get(token=kwargs['key'])
        if user and request.POST['password1'] == request.POST['password2']:
            user.user.set_password(request.POST['password2'])
            user.user.save()
            return redirect('/accounts/login/')
        else:
            messages.success(request, 'Please Make Sure Two password Fields are Same')
        return render_to_response(self.template_name, context_instance=RequestContext(request),)

class UpdateProfile(UpdateView):
    template_name = 'accounts/my-profile.html'
    form_class = ProfileUpdateForm

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        profile = UserProfiles.objects.get(user=user)
        id = user.id
        form = self.form_class({'first_name': profile.user.first_name, 'last_name': profile.user.last_name, 'email': profile.user.email,
                                'country': profile.country, 'mobile': profile.mobile, 'skypeid': profile.skypeid})
        return render_to_response(self.template_name, {'form': form, 'id': id, 'profile': profile}, context_instance=RequestContext(request),)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        site = Site.objects.get(pk=1)
        t = loader.get_template('accounts/verify.txt')
        profile = UserProfiles.objects.get(user=user)
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            if form.cleaned_data['mobile'] == None:
                profile.mobile = 0
            else:
                profile.mobile = request.POST.get('mobile')
            profile.skypeid = request.POST['skypeid']
            profile.country = request.POST['country']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.username = request.POST['email']
            if not str(request.user.email) == str(request.POST['email']):
                profile.email_verify = False
            user.save()
            profile.save()
            c = Context({'name': user.first_name, 'email':user.email, 'site': site.name, 'token': profile.token})
            send_mail('[%s] %s' % (site.name, 'User Updation Profile'), t.render(c), settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            messages.success(request, 'Profile Editted Successfully.')
            return redirect('/accounts/update-profile/')
        return render_to_response(self.template_name, {'form': form, 'id': id}, context_instance=RequestContext(request))


class MyPlan(TemplateView):

    template_name = 'accounts/my-plan.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not UserSubscriptions.objects.filter(user=self.request.user).exists():
            return redirect('/accounts/subscribe/?profile=true')
        return super(MyPlan, self).dispatch(*args, **kwargs)

    def get_plan(self, *args, **kwargs):
        plan = UserSubscriptions.objects.get(user=self.request.user)
        subscribed_plan = SubscriptionPlan.objects.get(id=plan.plan.id)
        return subscribed_plan

    def get_context_data(self, **kwargs):
        context = super(MyPlan, self).get_context_data(**kwargs)
        context['plan'] = self.get_plan()
        return context


class Settings(TemplateView):
    template_name = 'accounts/setting.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Settings, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        result={}
        user = UserProfiles.objects.get(user=request.user)
        if 'emailon' in request.POST and request.POST.get('emailon') == 'on':
            user.emailalert = True
            user.save()
            result['status'] = "success"
            result['message'] = "Settings Suceessfully updated"
        elif 'emailoff' in request.POST and request.POST.get('emailoff') == 'off':
            user.emailalert = False
            user.save()
            result['status'] = "success"
            result['message'] = "Settings Suceessfully updated"
        else:
            result['status'] = "failure"
            return HttpResponse(json.dumps(result), content_type='application/json')
        return HttpResponse(json.dumps(result), content_type='application/json')

    def get_emailstatus(self,  *args, **kwargs):
        users = UserProfiles.objects.get(user=self.request.user)
        return users.emailalert

    def get_context_data(self,  *args, **kwargs):
        context = super(Settings, self).get_context_data(**kwargs)
        context['staffs'] = self.get_emailstatus()
        return context



def save_settings(request):
    result={}
    print "adsdadsd"
    if request.method ==  'POST':
        email = request.POST.get('email')
        if request.POST.get('email'):
            result['status'] = "success"
            result['message'] = "Successfully Registered Will Contact you Soon!!!!"
        else:
            result['status']='failure'
            return HttpResponse(json.dumps(result),mimetype='application/json')
    return HttpResponse(json.dumps(result),mimetype='application/json')

class ChangePlan(TemplateView):
    template_name = 'accounts/change-plan.html'

    def get_context_data(self, **kwargs):
        context = super(ChangePlan, self).get_context_data(**kwargs)
        context['plans'] = SubscriptionPlan.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        try:
            user = UserSubscriptions.objects.get(user=request.user)
            plan = SubscriptionPlan.objects.get(id=request.POST['plan'])
            user.plan = plan
            user.save()
            if plan.free_plan == True:
                return redirect('/accounts/update-profile/')
            else:
                return redirect('/accounts/thanku/')
        except:
            pass
        return render_to_response(self.template_name, context_instance = RequestContext(request))

class ChangePassword(TemplateView):
    template_name = 'accounts/password-change.html'

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        username = user.username
        if user and request.POST['password1'] == request.POST['password2']:
            password = request.POST['password2']
            user.set_password(request.POST['password2'])
            user.save()
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/accounts/update-profile/')
        else:
            messages.success(request, 'Please Make Sure Two password Fields are Same')
        return render_to_response(self.template_name, context_instance=RequestContext(request),)

class About(TemplateView):
    template_name = 'about-us.html'


class Contact(TemplateView):
    template_name = 'contact-us.html'

    def post(self, request, *args, **kwargs):
        site = Site.objects.get(pk=1)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        t = loader.get_template('posts/contact.txt')
        c = Context({'name': name, 'email': email,
                     'site': site.name,
                    'message': message})
        send_mail('[%s] %s' % (site.name, 'New Contact Request'), t.render(c),
                  settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL], fail_silently=False)
        return render_to_response(self.template_name, context_instance=RequestContext(request))


@csrf_exempt
def checkout(request):
    print "sdsdd"
    template_name = 'accounts/thank-you.html'
    site = Site.objects.get(pk=1)
    plan = UserSubscriptions.objects.get(user=request.user)
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": plan.plan.price,
        "item_name": plan.plan.title,
        "invoice": int(randint(100,99999)),
        "notify_url": "https://%s"%(site.name) + reverse('paypal-ipn'),
        "return_url": "http://%s/accounts/update-profile"%(site.name),
        "cancel_return": "http://%s"%(site.name) ,

    }
    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    # form1 = CreditCardForm()
    # context = {"form": form,"course":course,"form1":form1,'name':name,'discount':discount,'message':message}
    return render(request, template_name, context)
    return render_to_response(template_name, context_instance=RequestContext(request))

@require_POST
@csrf_exempt
def custom_ipn(request, item_check_callable=None):

    '''
    django paypal view to store the IPN . the notify url excecutes this view.
    '''

    """
    PayPal IPN endpoint (notify_url).
    Used by both PayPal Payments Pro and Payments Standard to confirm transactions.
    http://tinyurl.com/d9vu9d

    PayPal IPN Simulator:
    https://developer.paypal.com/cgi-bin/devscr?cmd=_ipn-link-session
    """
    #TODO: Clean up code so that we don't need to set None here and have a lot
    #      of if checks just to determine if flag is set.
    flag = None
    ipn_obj = None

    # Clean up the data as PayPal sends some weird values such as "N/A"
    # Also, need to cope with custom encoding, which is stored in the body (!).
    # Assuming the tolerate parsing of QueryDict and an ASCII-like encoding,
    # such as windows-1252, latin1 or UTF8, the following will work:

    encoding = request.POST.get('charset', None)

    if encoding is None:
        flag = "Invalid form - no charset passed, can't decode"
        data = None
    else:
        try:
            data = QueryDict(request.body, encoding=encoding)
        except LookupError:
            data = None
            flag = "Invalid form - invalid charset"

    if data is not None:
        date_fields = ('time_created', 'payment_date', 'next_payment_date',
                       'subscr_date', 'subscr_effective')
        for date_field in date_fields:
            if data.get(date_field) == 'N/A':
                del data[date_field]

        form = PayPalIPNForm(data)
        if form.is_valid():
            try:
                #When commit = False, object is returned without saving to DB.
                ipn_obj = form.save(commit=False)
                # ipn_obj.user_name=request.user.email
                # ipn_obj.save()
            except Exception as e:
                flag = "Exception while processing. (%s)" % e
        else:
            flag = "Invalid form. (%s)" % form.errors

    if ipn_obj is None:
        ipn_obj = PayPalIPN()
        # ipn_obj.user_name=request.user.email
        # ipn_obj.save()
    #Set query params and sender's IP address
    ipn_obj.initialize(request)

    if flag is not None:
        #We save errors in the flag field
        ipn_obj.set_flag(flag)
    else:
        # Secrets should only be used over SSL.
        if request.is_secure() and 'secret' in request.GET:
            ipn_obj.verify_secret(form, request.GET['secret'])
        else:
            ipn_obj.verify(item_check_callable)
    ipn_obj.save()
    return HttpResponse("OKAY")


class CardPayment(TemplateView):
    template_name = 'accounts/credit-payment.html'
    form_class = StripeExtendededForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        card = request.POST.get('credit_card_number')
        month = request.POST.get('credit_card_expiration_month')
        year = request.POST.get('credit_card_expiration_year')
        cvv = request.POST.get('credit_card_cvc')
        plan = UserSubscriptions.objects.get(user=request.user)
        amount = int(plan.plan.price)
        if form.is_valid():
            stripe = get_gateway("stripe")
            credit_card = CreditCard(first_name="Test", last_name="User", month=month, year=year,
                             number=card,
                             verification_value=cvv)
            resp = stripe.purchase(int(amount), credit_card)
            print "resposne", resp['status']
            return redirect('/accounts/update-profile/')

        else:
            print "error", form.errors
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))




