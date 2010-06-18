"""
Tagging related views.
"""
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from tagging.models import Tag, TaggedItem, RelatedTag
from tagging.utils import get_tag, get_queryset_and_model

try:
    import json # comes with python 2.6
except ImportError:
    import simplejson as json

def tagged_item_list(request, queryset_or_model=None, tag_slug=None, 
                     content_type_id=None, **kwargs):
    """
    A thin wrapper around ``list_detail.object_list`` which returns a
    ``QuerySet`` containing instances of TaggedItem.

    In addition to the context variables set up by ``object_list``, a
    ``tag`` context variable will contain the ``Tag`` instance for the
    tag.
    """

    tag_slug = tag_slug or kwargs.get('tag')
    tag = get_object_or_404(Tag, slug=tag_slug)

    # check if is forwarded
    try:
        forward_tag = RelatedTag.objects.get(tag=tag, relation_type='=>')
    except RelatedTag.DoesNotExist:
        pass
    else:
        return HttpResponseRedirect(forward_tag.related_tag.get_absolute_url)
    
    ctype = None
    queryset_or_model = queryset_or_model or kwargs.get('queryset_or_model')
    if queryset_or_model:
        ctype = ContentType.objects.get_for_model(queryset_or_model)
    else:
        content_type_id = content_type_id or kwargs.get('content_type_id')
        if content_type_id:
            ctype = get_object_or_404(ContentType, id=content_type_id)
    
    queryset = TaggedItem.objects.filter(tag=tag)
    if ctype:
        queryset = TaggedItem.objects.filter(content_type=ctype)

    if not kwargs.has_key('extra_context'):
        kwargs['extra_context'] = {}
    kwargs['extra_context']['tag'] = tag

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
