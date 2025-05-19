from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.conf import settings
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin # used to protect routes from unauthenticated users.
from accounts.models import Post,UserProfile
from django.utils.timesince import timesince



def signin(request):
    if request.method == 'POST': #POST request is used to submit login credentials
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password) #verifies if a user with the given credentials exixts.
        if user is not None: #Returns a user object if credentials are valid, else returns None.
            auth.login(request,user) #logs the user in using django's auth.login()
            return redirect("index") #redirects to homepage
        else:
            messages.info(request,'Username or Password is incorrect')
            return redirect("signin")
            
    return render(request,"accounts/signin.html") #if the request is GET (shows the login form)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2: #Ensures that pssword and password2 match before continuing
            if User.objects.filter(username=username).exists(): #checks if the username already exists
                messages.info(request,"Username already Exists")
                return redirect('signup') #user exists and redirec to singup form
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already Exists")
                return redirect('signup')
            else:
                User.objects.create_user(username=username,email=email,password=password).save() #create_user() automatically hashes the password and saves the user safely.
                return redirect('signin')
        else:
            messages.info(request,"Password should match")
            return redirect('signup')
            
    return render(request,"accounts/signup.html") #Displays the signup form if the user is just visiting the page.



def logout(request):  #logs the user out using Django's built-in auth.logout()
    auth.logout(request) #Ends the user's session
    return redirect('index')

class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, id):
        user_obj = get_object_or_404(User, id=id)
        profile, _ = UserProfile.objects.get_or_create(user=user_obj)
        user_posts = Post.objects.filter(user=user_obj)
        total_likes = sum(post.likes for post in user_posts)

        context = {
            'user_obj': user_obj,
            'profile': profile,
            'posts': user_posts,
            'media_url': settings.MEDIA_URL,
            'total_posts': user_posts.count(),
            'total_likes': total_likes,
            'joined': timesince(user_obj.date_joined).split(',')[0] + " ago",
        }
        return render(request, 'accounts/profile.html', context)

class UserProfileEditView(LoginRequiredMixin, View):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        profile = get_object_or_404(UserProfile, user=user)  # FIXED

        if request.user != user:
            messages.warning(request, "You are not authorized to edit this profile.")
            return redirect('profile', id=request.user.id)

        return render(request, 'accounts/edit_profile.html', {
            'user': user,
            'profile': profile
        })

    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        profile = get_object_or_404(UserProfile, user=user)  # FIXED

        if request.user != user:
            messages.warning(request, "You are not authorized to edit this profile.")
            return redirect('profile', id=request.user.id)

        # Update User fields
        user.first_name = request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        user.email = request.POST.get('email')
        user.save()

        # Update UserProfile fields
        profile.bio = request.POST.get('bio')
        profile.facebook = request.POST.get('facebook')
        profile.twitter = request.POST.get('twitter')
        profile.linkedin = request.POST.get('linkedin')
        profile.instagram = request.POST.get('instagram')

        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES.get('profile_picture')

        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('profile', id=user.id)