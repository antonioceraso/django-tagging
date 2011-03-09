from django.conf.urls.defaults import *


urlpatterns = patterns('tagging.views',
    url(r'^ac/$', 'search_autocomplete', name='tag_search_ac'),
    url(r'^ac/(?P<category_slug>[-\w]+)/$', 'search_autocomplete', name='tag_search_ac_category'),
    url(r'^(?P<tag_slug>[-+\w]+)/$', 'taggeditem_list', name='tag_detail'),
    url(r'^(?P<app_name>([\w]+))/(?P<tag_slug>[-+\w]+)/$', 'taggeditem_list', name='tag_app_list'),
)
