"""
Tagging related views.
"""
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.db.models import Count
from tagging.models import Tag, TaggedItem, RelatedTag
from tagging.utils import get_tag, get_queryset_and_model, get_tags_from_slug
from tagging import settings

try:
    import json # python 2.6
except ImportError:
    import simplejson as json # python < 2.6


def tagged_item_list(request, queryset_or_model=None, tag_slug=None, 
                     content_type_id=None, app_name=None, **kwargs):
    """
    A thin wrapper around ``list_detail.object_list`` which returns a
    ``QuerySet`` containing instances of TaggedItem.

    In addition to the context variables set up by ``object_list``, a
    ``tags`` context variable will contain the ``Tag`` instances.
    """
    
    tag_slug = tag_slug or kwargs.get('tag')
    tags = get_tags_from_slug(tag_slug)
    
    if not queryset_or_model:
        if app_name:
            app_label, model_name = settings.TAGGING_APP_MAP[app_name].split('.')
            content_type_id = ContentType.objects.get_by_natural_key(app_label, model_name).id
        if content_type_id:
            queryset_or_model = ContentType.objects.get_for_id(content_type_id).model_class()

    queryset = TaggedItem.objects.get_by_model(queryset_or_model, tags)

    if not kwargs.has_key('extra_context'):
        kwargs['extra_context'] = {}
    kwargs['extra_context']['tags'] = tags
    kwargs['extra_context']['tag_slug'] = tag_slug
    kwargs['extra_context']['related_tags'] = RelatedTag.objects.get_related(tags)
    kwargs['extra_context']['app_name'] = app_name
    
    return object_list(request, queryset, **kwargs)


def search_autocomplete(request, category_slug):
    q = request.GET.get('tag')
    dump = ''
    if q:
        tags = Tag.objects.filter(name__icontains=q).order_by('-usage')
        tag_list = [] 
        for t in tags:
            tag_list.append({"caption": t.name, "value": t.slug})
        dump = json.dumps(tag_list)
    return HttpResponse(dump, mimetype="text/plain")


