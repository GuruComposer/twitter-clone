import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from network.forms import NewPostForm
from network.models import Post
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator


from .models import User

class Index(View):
    def get(self, request):
        success_url = "network/index.html"

        # pagination
        page_obj = paginatorAll(request)

        # Give the user the post form if they are logged in.
        if request.user.is_authenticated: 
            post_form = NewPostForm()
            ctx = {
                'page': "all-posts",
                'post_form': post_form,
                'posts': page_obj,}
            return render(request, success_url, ctx)
        # User is not logged in so don't display the post form.
        else: 
            ctx = {
                'page': "default",
                'posts': page_obj,}
            return render(request, success_url, ctx)
    
    def post(self, request):
        post_form = NewPostForm(request.POST)
        if post_form.is_valid():
            post_form.instance.owner = request.user
            post_form.save()
        return HttpResponseRedirect(reverse("index"))

class ProfileView(View):
    def get(self, request, username):
        profile = User.objects.get(username=username)

        # pagination
        page_obj = paginatorUser(request, profile.id)

        ctx = {
            'page': "profile",
            'posts': page_obj,
            'profile': profile}
        return render(request, "network/index.html", ctx)

class Following(LoginRequiredMixin, View):
    def get(self, request):

        # pagination
        page_obj = paginatorFollowing(request)

        ctx = {
            'page': 'following',
            'posts': page_obj,
        }
        return render(request, "network/index.html", ctx)


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
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")



### Api routes
### ------------------
@csrf_exempt
@login_required
def follow(request, user_id):

    # Query for requested user
    try:
        followee = User.objects.get(id=user_id)
        print(f"followee: {followee}")
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    # Return user contents
    if request.method == "GET":
        return JsonResponse(followee.serialize())

    # Update whether followee is followed or not
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("new_follower_id") is not None:
            new_follower_id = data["new_follower_id"]
        user = User.objects.get(id=request.user.id)

        # Toggle follwee's membership from user's followers field.
        if followee in user.follows.all():
            print(f"UNFOLLOW: {request.user} will unfollow: {new_follower_id}")
            user.follows.remove(followee)
            user.save()
            followee_follows_count = followee.followers.all().count()
            return JsonResponse({
                "follow-button-text": "Follow",
                "username": followee.username.capitalize(),
                "followee_follows_count": followee_follows_count,
                })
        else:
            print(f"FOLLOW: {request.user} will follow: {new_follower_id}")
            user.follows.add(followee)
            user.save()
            followee_follows_count = followee.followers.all().count()
            return JsonResponse({
                "follow-button-text": "Unfollow",
                "username": followee.username.capitalize(),
                "followee_follows_count": followee_follows_count,
                })

        

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@csrf_exempt
@login_required
def update_post(request, post_id):

    # Query for requested user
    try:
        post = Post.objects.get(id=post_id)
        print(f"post: {post}")
    except User.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return user contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update post
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("text") is not None:
            edited_text = data["text"]
            print(f"User: {request.user} edited their post to say: {edited_text}")
            post.text = edited_text
        elif data.get("liked") is not None:
            edited_like = data["liked"]
            print(f"User: {request.user} liked post#: {post.id}")
            print(post.likes.all())
            if (request.user in post.likes.all()):
                post.likes.remove(request.user)
            
            else:
                post.likes.add(request.user)
            
        post.save()
        print(post.likes.all().count())
        like_count = post.likes.all().count()
        return JsonResponse({"data": like_count})


    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


### Utility Functions
### ------------------
def query_all_posts():
    return Post.objects.all().order_by('-timestamp')

def query_user_posts(user_pk):
    return Post.objects.filter(owner=user_pk).order_by('-timestamp')

# pagination
def paginatorAll(request):
    post_list = query_all_posts()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

def paginatorUser(request, pk):
    post_list = query_user_posts(pk)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

def paginatorFollowing(request):
    print(request.user.follows.values_list('id', flat=True).distinct())
    follower_user_ids = request.user.follows.values_list('id', flat=True)
    print(Post.objects.filter(owner__in=follower_user_ids))
    post_list = Post.objects.filter(owner__in=follower_user_ids).order_by('-timestamp')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
