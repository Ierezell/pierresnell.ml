from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required


def last_posts(request):
    posts = Post.objects.order_by('-published_date')[:5]
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()
                                ).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, post_nb):
    post = get_object_or_404(Post, pk=post_nb)
    return render(request, 'blog/post_detail.html', {'post': post})


def commenter(request, post_nb):
    post = get_object_or_404(Post, pk=post_nb)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('blog:post_detail', kwargs={'post_nb': post.pk}))
    else:
        form = CommentForm()
    return render(request, 'blog/addcomment.html', {'form': form})
    # score = request.POST.get('note')
    # commentaire = request.POST.get('commentaire')
    # print(score)
    # print(commentaire)
    # if score == None:
    #     return render(request, 'blog/addcomment.html',
    #                   {'post': post,
    #                    'error_message': "Il faut renseignez la note !"
    #                    })
    # elif commentaire == '':
    #     return render(request, 'blog/addcomment.html',
    #                   {'post': post,
    #                    'error_message': "Il faut renseignez le commentaire !"
    #                    })
    # elif len(commentaire) < 10:
    #     return render(request, 'blog/addcomment.html',
    #                   {'post': post,
    #                    'error_message': "Allez un effort faites un vrai commentaire !"
    #                    })
    # else:
    #     print(f"({post.note}*{post.nb_vote})/{post.nb_vote+1}+{int(score)}/{post.nb_vote+1}")

    #     post.note = (post.note*post.nb_vote)/(post.nb_vote+1)+int(score)/(post.nb_vote+1)
    #     post.nb_vote += 1
    #     post.save()
    #     print(post.note)
    #     return HttpResponseRedirect(reverse('blog:post_list'))


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
            return HttpResponseRedirect(reverse('blog:post_detail', kwargs={'post_nb': post.pk}))
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_new_post.html', {'form': form})
