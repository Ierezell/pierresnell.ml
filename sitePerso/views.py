from django.utils.encoding import smart_str
import os
import glob
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.urls import reverse
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required


def acceuil(request):
    return render(request, 'sitePerso/acceuil.html')


def contact(request):
    return render(request, 'sitePerso/contact.html')


def projets(request):
    return render(request, 'sitePerso/projets.html')


def things(request):
    return render(request, 'sitePerso/things.html')


def professional(request):
    return render(request, 'sitePerso/professional.html')


def last_posts(request):
    posts = Post.objects.order_by('-published_date')[:5]
    return render(request, 'sitePerso/post_list.html', {'posts': posts})


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()
                                ).order_by('published_date')
    return render(request, 'sitePerso/post_list.html', {'posts': posts})


def post_detail(request, post_nb):
    post = get_object_or_404(Post, pk=post_nb)
    return render(request, 'sitePerso/post_detail.html', {'post': post})


def commenter(request, post_nb):
    post = get_object_or_404(Post, pk=post_nb)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('blog:post_detail',
                                                kwargs={'post_nb': post.pk}))
    else:
        form = CommentForm()
    return render(request, 'blog/addcomment.html', {'form': form})


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            print("WOUHOUUUUUUUUUU")
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return HttpResponseRedirect(reverse('blog:post_list'))
    else:
        form = PostForm()
    return render(request, 'blog/edit_new_post.html', {'form': form})


@login_required
def edit_post(request, post_nb):
    post = get_object_or_404(Post, pk=post_nb)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return HttpResponseRedirect(reverse('blog:post_detail',
                                                kwargs={'post_nb': post.pk}))
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_new_post.html', {'form': form})


@login_required
def view_files(request, path='default'):
    if path == 'default':
        globed = glob.glob("./media/*")
        parent = ""
    else:
        globed = glob.glob(f"./media/{path.replace('+','/')}/*")
        parent = path
    folders = [f.split("/")[-1] for f in globed if os.path.isdir(f)]
    files = [f.split("/")[-1] for f in globed if os.path.isfile(f)]
    print(folders)
    print(files)
    return render(request, 'sitePerso/files.html', {"folders": folders,
                                                    "files": files,
                                                    "parent": parent})


@login_required
def download(request, path):
    path = path.strip("+")
    path_to_file = path.replace("+", "/")
    file_name = path_to_file.split("/")[-1]
    # mimetype is replaced by content_type for django 1.7
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(
        file_name)
    response['X-Accel-Redirect'] = smart_str(path_to_file)

    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response
