import datetime
from django.utils import timezone
from .models import Post, Comment, PostLike, Opinion, User
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
#Recebe requisição


@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date') 
    return render(request, 'blog/post_list.html', {'posts':posts})
    
@login_required
def post_detail (request, pk):
    post = get_object_or_404(Post, pk=pk)

    post.views += 1
    post.save()


    cont_likes_total = post.likes_count()

    cont_deslikes_total = post.deslikes_count()

    percentApproval = 0
    percentDisapproval = 0

    if not cont_likes_total == 0 and cont_deslikes_total == 0 : 

        percentApproval = cont_likes_total / ( cont_likes_total + cont_deslikes_total) * 100

        percentDisapproval = cont_deslikes_total / ( cont_deslikes_total +  cont_likes_total) * 100


    if percentApproval < 0:
        percentApproval = 0
    
    elif percentDisapproval < 0:
        percentDisapproval = 0

    print('Aprroval:', percentApproval)
    print('Disapprova: ',percentDisapproval)

    return render(request, 'blog/post_detail.html',{'post': post, 'approval': percentApproval, 'disapproval': percentDisapproval})




@login_required
def post_new(request):

    if request.method == "POST":
         form = PostForm(request.POST)
         if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    post = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'post': post})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def publish(self):
    self.published_date = timezone.now()
    self.save()

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@login_required
def post_like(request, pk):

    try:
        op = Opinion.objects.filter(post_id = pk, user= request.user).values()


        if len(op) == 0 :
            opinion = Opinion.objects.create(post_id=pk, user= request.user, like = 1, deslike = 0)
            opinion.save()

        else:
            print(op[0]['id'])
            auxOp = Opinion.objects.get(id = op[0]['id'])
          
            if auxOp.deslike >= 1:
                auxOp.deslike -=1
                auxOp.like += 1
            
            auxOp.save()

    except Opinion.DoesNotExist :
        opinion = Opinion.objects.create(post_id=pk, user= request.user, like = 1, deslike = 0)
        opinion.save()

    return redirect('post_detail', pk = pk) 


@login_required
def post_deslike(request, pk):

    try:
        op = Opinion.objects.filter(post_id = pk, user= request.user).values()


        if len(op) == 0 :
            opinion = Opinion.objects.create(post_id=pk, user= request.user, like = 0, deslike = 1)
            opinion.save()

        else:
            auxOp = Opinion.objects.get(id = op[0]['id'])
            if auxOp.like >= 1:
                auxOp.deslike +=1
                auxOp.like -= 1
            
            auxOp.save()

    except Opinion.DoesNotExist :
        opinion = Opinion.objects.create(post_id=pk, user= request.user, like = 0, deslike = 1)
        opinion.save()

    return redirect('post_detail', pk = pk) 

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)