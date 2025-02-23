from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden , JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator

from .models import Post
from .forms import CreatePost,CreateComment
# Create your views here.
@login_required(login_url = '/accounts/login')
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # categories = Post.objects.values_list('category', flat=True).distinct()
    topic_counts = Post.objects.values('topic').annotate(post_count=Count('id')).order_by('topic')
    return render(request,'posts/post_list.html',{'posts':page_obj,'topic_counts':topic_counts})

def post_page(request,postid):
    post = get_object_or_404(Post,id=postid)
    related_posts = Post.objects.filter(topic__iexact=post.topic).exclude(id=post.id).order_by('-created_at')[:2]
    if request.method == 'POST':
        form = CreateComment(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('posts:post-page',post.id)
    else:
        form = CreateComment()
    comments = post.comments.all()
    context = {'post' : post,'comments':comments,'form':form,'related_posts':related_posts}
    return render(request,'posts/post_page.html',context)

@login_required(login_url = '/accounts/login')
def create_post(request):
    if request.method == 'POST':
        form = CreatePost(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, "Your post has been created successfully!")
            return redirect('posts:post-list')
    else:
        form = CreatePost()
    return render(request,'posts/create_post.html',{'form' : form})


def update_post(request,postid):
    post = get_object_or_404(Post,id=postid)
    if request.method == 'POST':
        form = CreatePost(request.POST,instance = post)
        if form.is_valid():
           form.save()
           messages.success(request, "Your post has been updated successfully!")
           return redirect('posts:post-list')
    else:
        form = CreatePost(instance = post)
        return render(request,'posts/create_post.html',{'form':form,'post':post})
    

@require_POST
def delete_post(request,postid):
    post = get_object_or_404(Post,id=postid)
    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to delete this post")
    post.delete()
    messages.success(request, "Your post has been deleted successfully!")
    return redirect('posts:post-list')

def search_post(request):
    query = request.GET.get('q')
    post_type = request.GET.get('post_type')
    topic_counts = Post.objects.values('topic').annotate(post_count=Count('id')).order_by('topic')
    if post_type == 'all':
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(post_type = post_type)

    if query:
        posts = posts.filter(title__icontains = query)
    
    context = {
        'posts':posts,
        'query' : query,
        'post_type':post_type,
        'topic_counts':topic_counts
    }

    return render(request,'posts/post_list.html',context)


def topic_search(request,topic):
    posts = Post.objects.filter(topic = topic)
    topic_counts = Post.objects.values('topic').annotate(post_count=Count('id')).order_by('topic')
    return render(request,'posts/post_list.html',{'posts':posts,'topic_counts':topic_counts})


@login_required(login_url = '/accounts/login')
@require_POST
def toggle_like(request,postid):
    # post_id = request.GET.get('post_id')
    post = get_object_or_404(Post,id=postid)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    
    else:
        post.likes.add(user)
        liked = True
    
    data = {
        'liked':liked,
        'total_likes':post.total_likes(),
    }

    return JsonResponse(data)