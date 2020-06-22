from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from django.contrib.auth import get_user_model as user
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity


from .models import Post, Comment
from .forms import CommentForm, SearchForm
# Create your views here.


#@login_required
def post_detail(request, post, pk):
    post = get_object_or_404(Post, id=pk, slug=post, status='published')
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request,
        'post_detail.html',
        {'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts})


'''class PostDetailView(LoginRequiredMixin, DetailView):
    queryset = Post.published.all()
    template_name = 'post_detail.html'
    context_object_name = 'post'
    query_pk_and_slug = True
    login_url = 'login'
'''
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = ('title', 'body',)
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


'''class PostListView(LoginRequiredMixin, ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'post_list.html'
    login_url = 'login' '''

@login_required
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 5) # 5 posts in each page
    is_paginated = True if paginator.num_pages > 1 else False
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                 'post_list.html',
                 {'page': page,
                 'is_pagenated': is_paginated,
                 'paginator': paginator,
                  'posts': posts,
                  'tag': tag})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('title', 'body',)
    template_name = 'post_edit.html'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


# view to handle my email sending form in forms.py

class CommentUpdateView(UpdateView):
    model = Comment
    fields = ('comment',)
    template_name = 'comment_edit.html'


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'comment_delete.html'

    def get_success_url(self):
        post = Post.objects.get(pk=self.object.post.pk)
        return post.get_absolute_url()


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
                ).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request,
        'post_search.html',
        {'form': form,
        'query': query,
        'results': results})






