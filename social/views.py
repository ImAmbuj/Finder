import os
from .models import User,Post, Follower
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.
def index(request):
 if request.user.is_authenticated:
    return redirect('/Home')  
 else:    
        if request.method=='POST' :
            if "register" in request.POST:  
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                username = request.POST['username']
                email = request.POST['email']
                password = request.POST['password']
         
                
                if get_user_model().objects.filter(username=username).exists():
                    messages.info(request, 'Username Taken ')
        
                    return redirect('/Accounts')
                elif get_user_model().objects.filter(email = email).exists():
                     messages.info(request, 'Email Taken')
                     return redirect('/Accounts')
                else:
                     new_account = get_user_model().objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                     new_account.save()
                     Follower.objects.create(user=new_account)
                     messages.info(request, 'User Created ')
                     print('User created')
             
            elif "login" in request.POST:
    
                username = request.POST['username']
                password = request.POST['password']
               
                user = auth.authenticate(username = username, password = password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('/Home')
                else:
                    messages.error(request, 'User Not Found')
                    return redirect('/Accounts')    
    
        return render(request, 'account.html')


@login_required(login_url="/")
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url="/")
def home(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            post_text = request.POST.get('post_text', '')
            post_img = request.FILES.get('post_img', '')
        
            new_post = Post(creator= request.user, post_img = post_img,post_text= post_text )
            new_post.save()

        followingof_user = Follower.objects.filter(followers=request.user).values('user')
        all_posts = Post.objects.filter(creator__in=followingof_user).order_by('-date_created')  | Post.objects.filter(creator=request.user).order_by('-date_created')
        user_data = get_user_model().objects.get(username=request.user)

        return render(request,'home.html',{"all_posts":all_posts,"user_data":user_data})

    else:
                return redirect('/Accounts')

@login_required(login_url="/")
def profile(request, username):
    if request.user.is_authenticated:
        if request.method == 'POST':
            bio = request.POST.get('bio')
            profile_image = request.POST.get('profile_image')
            
            try:
                get_user_model().objects.filter(username=request.user).update(bio=bio, profile_pic=profile_image )
            except Exception as error:
                return HttpResponse(error) 
        

    user = get_user_model().objects.get(username=username)
    all_posts = Post.objects.filter(creator=user).order_by('-date_created')
    follower = False

    if request.user in Follower.objects.filter(user=user).first().followers.all():
                follower = True

    follower_count = Follower.objects.filter(user=user).first().followers.all().count()        
    following_count = Follower.objects.filter(followers=user).count() 

    data = {
        "username" : user,
        "all_posts" : all_posts,
        "post_count": all_posts.count(),
        "page" : "profile",
        "is_follower" : follower,
        "follower_count" : follower_count,
        "following_count" : following_count,
    }       

    return render(request, 'profilepage.html', data)

def users(request):
    all_users = get_user_model().objects.all()

    return render(request,'users.html',{'all_users': all_users})    


@login_required(login_url="/")
def handle_follows(request, username):
    user = get_user_model().objects.get(username=username)
    followers_of_user = Follower.objects.get(user=user)
    if followers_of_user.followers.filter(username=request.user).exists():
        followers_of_user.followers.remove(request.user)
        followers_of_user.save()
    else:
        followers_of_user.followers.add(request.user)
        followers_of_user.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/")
def handle_likes(request, id):
    get_post = Post.objects.get(id=id)
    if get_post.likers.filter(username=request.user).exists():
        get_post.likers.remove(request.user)
        get_post.save()

    else:
        get_post.likers.add(request.user)
        get_post.save()
     
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_post(request, id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=id)
        if request.user == post.creator:
            try:
                post.delete()
            except Exception as e:
                return HttpResponse(e)    

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    


@login_required(login_url="/")
def handle_saves(request, id):
    get_post = Post.objects.get(id=id)
    if get_post.savers.filter(username=request.user).exists():
        get_post.savers.remove(request.user)
        get_post.save()

    else:
        get_post.savers.add(request.user)
        get_post.save()
     
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def saved_posts(request):
    if request.user.is_authenticated:
        all_posts = Post.objects.filter(savers=request.user).order_by('-date_created')
    
    return render(request,'saves.html', {'all_posts': all_posts})

    