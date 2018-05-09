# -*-coding:utf-8-*-
from django.shortcuts import render, HttpResponse, get_object_or_404
import markdown
from comments.forms import CommentForm
from .models import Post, Category, Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.

def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html', context={'post_list': contacts })

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    md = markdown.Markdown(
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    post.body = md.convert(post.body)
    post.toc = md.toc
    form = CommentForm()
    comment_list = post.comment_set.all()
    return render(request, 'blog/detail.html', context={'post':post, 'form':form, 'comment_list':comment_list})

def archives(request, year, month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month,
                                    )
    return render(request, 'blog/index.html', context={'post_list':post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list':post_list})

def tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag)
    return render(request, 'blog/index.html', context={'post_list':post_list})

def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/index.html', {'error_msg':error_msg})
    post_list = Post.objects.filter(Q(title__icontains=q)|Q(body__icontains=q))
    return render(request, 'blog/index.html', {'post_list':post_list,'error_msg': error_msg})

def about(request):
    return render(request, 'blog/about.html')
