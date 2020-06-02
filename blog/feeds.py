from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy


from .models import Post


class LatesPostsFeed(Feed):
    title = 'Dvelopers Forum'
    link = reverse_lazy('post_list')
    description = 'New posts from Developers Forum'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
