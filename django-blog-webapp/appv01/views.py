from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import user,post,comment,reply,tag,tagpostjunc
from django.contrib.auth import logout
from django.shortcuts import redirect,get_object_or_404
import json
from django.contrib.auth import authenticate, login
import re
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F


# Create your views here.

def welcome(request):
    return HttpResponse("Helli from the appv01 !!")




def feed_func(request):
    try:
        all_posts = post.objects.all().order_by('-created_at')
        post_ids = all_posts.values_list('id', flat=True)
        all_junctions = tagpostjunc.objects.filter(post_id__in=post_ids).select_related('tag')
        for p in all_posts:
            p.manual_tags = [j.tag for j in all_junctions if j.post_id == p.id]
        context = {
            'posts': all_posts,
        }
        return render(request, 'appv01/feed.html', context)
    except Exception as e:
        messages.error(request, "The feed is currently unavailable. Please try again later.")
        return render(request, 'appv01/feed.html', {'posts': []})


def create_post_view(request):
    try:
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            tag_data = request.POST.get('tags', '')
            image_file = request.FILES.get('attachment')

            new_post = post.objects.create(
                author=request.user,
                title=title,
                content=content,
                attachment=image_file
            )

            tag_list = []
            
            if tag_data:
                split_data = re.split(r'[,\s]+', tag_data)
                for t in split_data:
                    clean_tag = t.strip().lower()
                    if clean_tag != "":
                        tag_list.append(clean_tag)

            for name in tag_list:
                tag_obj, _ = tag.objects.get_or_create(name=name)
                tagpostjunc.objects.get_or_create(post=new_post, tag=tag_obj)

            return JsonResponse({'status': 'success', 'message': 'Post created with tags!'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return render(request, 'appv01/createpost.html')

def login_view(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            try:
                user_found = user.objects.get(email=email)
                username = user_found.username
            except user.DoesNotExist:
                return JsonResponse({"status": "error", "message": "User not found"}, status=401)

            auth_user = authenticate(request, username=username, password=password)

            if auth_user is not None:
                login(request, auth_user)
                return JsonResponse({"status": "success"}, status=200)
            else:
                return JsonResponse({"status": "error", "message": "Incorrect password"}, status=401)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return render(request, 'appv01/login.html')



def registration_view(request):
    if request.method=='POST':
        print(f"DEBUG: Request Body is: {request.body}")
        try:
            data=json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')

            if not username or not password or not email:
                return JsonResponse({"status": "error", "message": "Missing required fields"}, status=400)

            if user.objects.filter(username=username).exists():
                return JsonResponse({"status": "error", "message": "Username already taken"}, status=400)
            
            user.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            return JsonResponse({"status": "success"}, status=201)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
        
    return render(request,'appv01/registration.html')


@login_required
def profile_view(request):
    try:
        print(f"DEBUG: Current User is {request.user}") 
        user_posts = post.objects.filter(author=request.user).order_by('-created_at')
        print(f"DEBUG: Found {user_posts.count()} posts")
        post_ids = user_posts.values_list('id', flat=True)
        all_junctions = tagpostjunc.objects.filter(post_id__in=post_ids).select_related('tag')
        for p in user_posts:
            p.manual_tags = [j.tag for j in all_junctions if j.post_id == p.id]
        context = {
            'posts': user_posts,
        }
        return render(request, 'appv01/feed.html', context)
    except Exception as e:
        messages.error(request, f"Could not load your posts: {e}")
        return render(request, 'appv01/feed.html', {'posts': []})




def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def like_post(request, post_id):
    if request.method == "POST":
        target_post = get_object_or_404(post, id=post_id)
        user = request.user
        
        if user in target_post.users_who_liked.all():
            target_post.users_who_liked.remove(user)
            liked = False
        else:
            target_post.users_who_liked.add(user)
            liked = True
            
        target_post.likes_count = target_post.users_who_liked.count()
        target_post.save()
        
        return JsonResponse({
            'success': True,
            'new_count': target_post.likes_count,
            'is_liked': liked
        })
    

@login_required
def comment_page(request, post_id):
    target_post = get_object_or_404(post, id=post_id)
    
    if request.method == "POST":
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id') 

        if content:
            if parent_id:
                parent_comment = get_object_or_404(comment, id=parent_id)
                reply.objects.create(
                    comment=parent_comment,
                    post=target_post,
                    commentator=request.user,
                    reply_content=content
                )
            else:
                comment.objects.create(
                    post=target_post,
                    commentator=request.user,
                    comment_content=content
                )
            return redirect('comment', post_id=post_id)

    all_comments = target_post.comments.all().prefetch_related('replies').order_by('-created_at')
    
    return render(request, 'appv01/comment.html', {
        'post': target_post,
        'comments': all_comments
    })

@login_required
def delete_comment(request, comment_id):
    target_comment = get_object_or_404(comment, id=comment_id)
    if target_comment.commentator == request.user:
        post_id = target_comment.post.id
        target_comment.delete()
        return redirect('comment', post_id=post_id)
    return redirect('feed')


def get_comment_count(request, post_id):
    try:
        target_post = get_object_or_404(post, id=post_id)
        count_comments = target_post.comments.count()
        count_replies = reply.objects.filter(post=target_post).count()
        
        return JsonResponse({
            'success': True,
            'total_count': count_comments + count_replies
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    

@login_required
def edit_post(request, post_id):
    target_post = get_object_or_404(post, id=post_id)
    
    if target_post.author != request.user:
        return redirect('feed')

    if request.method == "POST":
        target_post.title = request.POST.get('title')
        target_post.content = request.POST.get('content')
        
        if request.FILES.get('attachment'):
            target_post.attachment = request.FILES.get('attachment')
            
        target_post.save()
        return redirect('profile') 

    return render(request, 'appv01/edit_post.html', {'post': target_post})

@login_required
def delete_post(request, post_id):
    target_post = get_object_or_404(post, id=post_id)
    
    if target_post.author == request.user:
        target_post.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=403)