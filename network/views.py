import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


from .models import User, Post, Profile


def index(request):
    page_posts = Paginator(Post.objects.all(), 10)
    page_number = request.GET.get("page")
    if page_number != None:
        try:
            required_page = page_posts.page(page_number)
        except:
            required_page = page_posts.page(1)
    else: 
        required_page = page_posts.page(1)
    return render(request, "network/index.html", {
        "posts": required_page
    })

@login_required
def profile(request, user_id):
    key_user = User.objects.get(username=user_id)
    key = Profile.objects.get(user=key_user)
    print(key)
    page_posts = Paginator(Post.objects.filter(user=key_user), 10)
    page_number = request.GET.get("page")
    if page_number != None:
        try:
            required_page = page_posts.page(page_number)
        except:
            required_page = page_posts.page(1)
    else: 
        required_page = page_posts.page(1)
    return render(request, "network/profile.html", {
        "posts": required_page,
        "profile": key
    })

def get_full_name(self):
    return self.first_name + ' ' + self.last_name


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstName = request.POST["firstname"]
        lastName = request.POST["lastname"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = firstName
            user.last_name = lastName 
            user.save()
            profile = Profile(user=user)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
@csrf_exempt
def new_post(request):
    if request.method == "POST":
        post_data = json.loads(request.body)
        post_body = post_data.get("body", "")
        post = Post(
            user = request.user,
            body = post_body 
        )
        post.save()
        content = {
            'status': 201,
            'post_id': post.id,
            'username': request.user.username,
            'body': post.body,
            'likes': post.likes.all().count(),
            'timestamp': post.timestamp.strftime("%B %d, %Y, %I:%M %p")
        }
        return JsonResponse(content, status=201)
    return JsonResponse({"error":"Not POST method" }, status=400)

@login_required
@csrf_exempt
def follow(request):
    if request.method == "PUT":
        put_data =  json.loads(request.body)
        follow_username = put_data.get("user", "")
        follow_user = User.objects.get(username=follow_username)
        follow_profile = Profile.objects.get(user=follow_user)
        following_profile = Profile.objects.get(user=request.user)
        follow_action = put_data.get("follow_action","")
        if(follow_action == True):
            follow_profile.follower.add(request.user)
            following_profile.following.add(follow_user)
            print("follow")
        else:
            follow_profile.follower.remove(request.user)
            following_profile.following.remove(follow_user)
            print(follow_profile.follower)
        follow_profile.save()
        response = {
            "status": 201,
            "action": follow_action,
            "message": "Followed success"
        }
        return JsonResponse(response, status=201)
    return JsonResponse({"error":"Followed Failure"}, status=400)

@login_required
def following(request):
    profile = Profile.objects.get(user=request.user)
    following_users = profile.following.all()
    page_posts = Paginator(Post.objects.filter(user__in=following_users), 10)
    page_number = request.GET.get("page")
    if page_number != None:
        try:
            required_page = page_posts.page(page_number)
        except:
            required_page = page_posts.page(1)
    else: 
        required_page = page_posts.page(1)
    return render(request, "network/following.html", {
        "posts": required_page,
    })

@login_required
@csrf_exempt
def edit(request):
    if request.method == "PUT":
        put_data =  json.loads(request.body)
        post_ID = put_data.get("ID", "")
        target_post = Post.objects.get(pk=post_ID)
        if target_post.user != request.user:
            return JsonResponse({"error":"Restricted Action"}, status=401)
        else:
            target_post.body = put_data.get("body", "")
            target_post.save()
        return JsonResponse({"message":"Successfully edited",
        "body": target_post.body}, status=201)
    return JsonResponse({"error":"Followed Failure"}, status=400)


@login_required
@csrf_exempt
def like(request):
    if request.method == "PUT":
        put_data =  json.loads(request.body)
        post_ID = put_data.get("ID", "")
        target_post = Post.objects.get(pk=post_ID)
        if request.user not in target_post.likes.all():
            target_post.likes.add(request.user)
            return JsonResponse({"isLiked": True}, status=201)
        else:
            target_post.likes.remove(request.user)
            return JsonResponse({"isLiked": False}, status=201)
    return JsonResponse({"error":"Forbidden Request"}, status=401)
