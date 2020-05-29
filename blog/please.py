'''
This GCBV  is actually keeps things shorter for prefessional who already knows how to use it well.
As a beginner I am, i found FBV more understandable because I typically see he whole flow
which is not the case in GCBV where the heavy lifting has been done behind the scene, and which understanding 
how it works is the key.
You know the  one of the men am folowing his book to learn this used FBV for his post_detail and CBV for 
post_list. 
To me, at least currently, I understand GCBV and find it interesting only for CRUD. When it comes to handling forms
in CBV, i use to be lost (or I'm lost).

Now, I have made a comment system and want to instantiate it in the post_detail view.
handling this form is giving me issue... I believe I get over it after some practice.

You have captured my custom manager(published) with the queryset attribute of DetailView. Now, i have to 
filter the comments by 'active'.
I am tempted to pass a list into the queryset attributes but am unsure if it's legal.


'''

#This is the comment model I added to models 
class Comment(models.Model):
    user = get_user_model()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(user, on_delete=models.CASCADE,)
    body = models.TextField()    
    created = models.DateTimeField(auto_now_add=True)  
    updated = models.DateTimeField(auto_now=True)    
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'

#forms.py
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)

#This is what he has in his views.py

def post_detail(request, year, month, day, post): # Ignore this as you have showed me how to use pk & slug in the CBV
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    # List of active comments for this post
    #It's from that I want to add to my CBV that you helped me before.
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True) # I haven't reached here yet. see as it's easy adding things to FBV
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})



#tThis is what i currently have in my CBV equivalent
class PostDetailView(LoginRequiredMixin, DetailView):
    queryset = Post.published.all()
    template_name = 'post_detail.html'
    context_object_name = 'post'
    query_pk_and_slug = True
    login_url = 'login'


#This is what i currently have in my models.py for Post model
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.pk, self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
