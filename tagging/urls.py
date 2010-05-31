from django.conf.urls.defaults import *


urlpatterns = patterns('tagging.views',
    url(r'^search/$', 'tag_search', name='tag_search'),
    url(r'^search/ac/$', 'tag_search_autocomplete', name='tag_search_autocomplete'),
)
