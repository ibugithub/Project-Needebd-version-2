from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from validate_email import validate_email
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import  get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import generate_token, send_sms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login, authenticate 
from django.http.response import HttpResponseRedirect
from .forms import LoginForm
import threading
import re
from .forms import CodeForm
from core.models import CustomerProfile



# Create your views here.
User = get_user_model()

# <-------Regex for validating Phone number-------->

# regex = '^\+?1?\d{9,15}$'
# def check(email):
#     if re.search(regex, email):
#         return True
#     else:
#         return False

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


class RegistrationView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')
    
    def post(self, request):

        context = {
            'data': request.POST,
            'has_error':False
        }
        email = request.POST.get('email')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # if check(phone):
        #     pass
        # else:
        #     messages.add_message(request, messages.ERROR, "Phone number is Invalid")
        #     context['has_error'] = True

        if len(password) < 8:
            messages.add_message(request, messages.ERROR, 'password should be at least 8 characters long')
            context['has_error'] = True

        if password != password2:
            messages.add_message(request, messages.ERROR, "password don't match")
            context['has_error'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR,
                                 'Please provide a valid email')
            context['has_error'] = True

        try:
            if User.objects.get(email = email):
                messages.add_message(request,messages.ERROR, 'This Email is already taken')
                context['has_error'] = True
        except Exception as identifier:
            pass

        try:
            if User.objects.get(user_name=username):
                messages.add_message(request, messages.ERROR, 'This Username is already taken')
                context['has_error'] = True
        except Exception as identifier:
            pass

        try:
            if User.objects.get(phone_number = phone):
                messages.add_message(request, messages.ERROR, 'This Phone Number is already taken')
                context['has_error'] = True
        except Exception as identifier:
            pass

        if context['has_error']:
            return render(request, 'accounts/register.html', context, status =400)

        user = User.objects.create_user(email = email, user_name = username, phone_number = phone)
        user.set_password(password)
        # user.is_active = False
        user.save()

        current_site  = get_current_site(request)
        email_subject = 'Active your Account'
        message = render_to_string('accounts/active.html',
        {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        }
        )

        email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
        )

        EmailThread(email_message).start()
        messages.add_message(request, messages.SUCCESS, "You'll have to Verify your gmail first")
        return redirect('/accounts/login/')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_verified = True
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Email verified successfully')
            CustomerProfile(user = user, email = user.email, phone_number = user.phone_number).save()
            return redirect('/accounts/login/')
        return render(request, 'accounts/activate_failed.html', status=401)

def log_in(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = LoginForm(request = request, data = request.POST)
            if fm.is_valid():
                email = fm.cleaned_data['username']
                password = fm.cleaned_data['password']
                user = authenticate(username = email, password = password)
                if user is not None:
                    muser = User.objects.get(email = email)
                    if muser.is_verified == True:
                        login(request, user)                   
                        return redirect('/')
                    else:
                        request.session['forresendpk'] = muser.pk
                        return render(request, 'accounts/login2.html')
                    # request.session['pk'] =user.pk
                    # return redirect('/accounts/verify')
        else:
            fm = LoginForm()
        return render(request, 'accounts/login.html', {'form':fm})

    else:
        return render(request, 'accounts/profile.html')

def ResendGmailVerificationLink(request):
        pk = request.session.get('forresendpk') 
        user = User.objects.get(pk = pk)
        email = user.email        
        current_site  = get_current_site(request)
        email_subject = 'Active your Account'
        message = render_to_string('accounts/active.html',
        {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        }
        )

        email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
        )

        EmailThread(email_message).start()
        messages.add_message(request, messages.SUCCESS, "A verification link sent to your gmail account")
        return redirect('/accounts/login/')

# def verify_view(request):
#     form = CodeForm(request.POST or None)
#     pk = request.session.get('pk')
#     if pk:
#         user = User.objects.get(pk=pk)
#         code = user.code
#         code_user = f"{user.user_name}: {user.code}"
#         if not request.POST:

#             # send_sms(code_user, user.phone_number)
      
           
#             print(code_user)

#         if form.is_valid():
#             num = form.cleaned_data.get('number')
#             if str(code) == num:
#                 code.save()
#                 login(request, user)
#                 messages.add_message(request, messages.SUCCESS,
#                                     'account activated successfully')
#                 return redirect('/')
#             else:
#                 messages.add_message(request, messages.ERROR, 'Your Confirmation code was worng')
#                 return HttpResponseRedirect('/accounts/login')
#     return render(request, 'accounts/verify.html', {'form':form})            

def profile(request):
    return render(request, 'accounts/profile.html')

def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')
