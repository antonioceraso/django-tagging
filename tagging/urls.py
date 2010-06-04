from django.conf.urls.defaults import *


urlpatterns = patterns('tagging.views',
    url(r'^search/ac/$', 'search_autocomplete', name='tag_search_autocomplete'),
    url(r'^(?P<tag_slug>[-\w])/$', 'tagged_item_list', name='tag_detail'),
)
