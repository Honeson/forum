from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post, Comment


register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def total_comments():
    return Comment.objects.count()


@register.inclusion_tag('latest_comments.html')
def show_latest_comments(count=2):
    latest_comments = Comment.objects.order_by('-created')[:count]
    return {'latest_comments': latest_comments}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
        ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
