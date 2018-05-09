from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count

register = template.Library()
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-create_time')[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('create_time', 'day',  order='DESC')

@register.simple_tag
def get_category():
    return Category.objects.annotate(num_post=Count('post')).filter(num_post__gt=0)

@register.simple_tag
def get_tag():
    return Tag.objects.annotate(num_post=Count('post')).filter(num_post__gt=0)
