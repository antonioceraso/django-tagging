from django.conf.urls.defaults import *


urlpatterns = patterns('tagging.views',
    url(r'^ac/$', 'search_autocomplete', name='tag_search_ac'),
    url(r'^ac/(?P<category_slug>[-\w]+)/$', 'search_autocomplete', name='tag_search_ac_category'),
    url(r'^(?P<tag_slug>[-+\w]+)/$', 'tagged_item_list', name='tag_detail'),
)
