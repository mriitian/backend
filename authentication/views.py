from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from gfg import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import login
from .tokens import generate_token


def get_csrf_token(request):
    return get_token(request)

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

@csrf_exempt
def signup(request):
    if request.method=="POST" :
        #username= request.POST.get['username']
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 =request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username= username):
            messages.error(request, "Username already exists! Pleasetry some other usrename")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('home')
        
        if pass1!=pass2 :
            messages.error(request,"Password did not match")
        if len(username)>10 :
            messages.error(request, "Username must be under 10 letters ")
            
            
        if not username.isalnum():
            messages.error(request, "Username must be alph-numeric!")
            return redirect('home')
        
        
        myuser= User.objects.create_user(username, email, pass1)
        myuser.first_name=fname
        myuser.last_name = lname
        myuser.is_active= False 
        myuser.save()
        
        myuser.save()
        
        messages.success(request,"Your Account has been successfully created")
        #welcome Email
        
        subject = "Welcome to myweb-DJANGO Login!"
        
        message = "Hello"+myuser.first_name+" !!\n"+"Welcome to mywebb!!\n  Thank you for visiting our website \n We have also set you a conformtion email address in order to activate your gamil account\n "
          
        from_email = settings.EMAIL_HOST_USER 
        to_list = [myuser.email]
        send_mail(subject, message, from_email,to_list, fail_silently= True)     
        
        
        #Email Address Conformation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your email @ myweb. Django Login !!"
        message2= render_to_string('email_confirmation.html',{
            'name':myuser.first_name,
            'domain': current_site.domain,
            'utd':urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email= EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            {myuser.email}
        )
        email.fail_silently= True
        email.send()
        
        return redirect('signin')
        
        
    return render(request, "authentication/signup.html")

@csrf_exempt
def signin(request):
    if request.method =='POST':
        username= request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html",{'fname':fname})
        
            
        else:
            messages.error(request, "Bad credentials")
            return redirect('home')
    return render(request, "authentication/signin.html")

@csrf_exempt
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('home')

@csrf_exempt
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
        
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')
        