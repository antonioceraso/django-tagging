"""
Tagging related views.
"""
from django.http import Http404
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.utils.datastructures import SortedDict
from django.template import RequestContext
from tagging.models import Tag, TaggedItem, RelatedTag
from tagging.utils import get_tag, get_queryset_and_model, get_tags_from_slug
from tagging import settings

try:
    import json # python 2.6
except ImportError:
    import simplejson as json # python < 2.6


def tagged_object_list(request, queryset_or_model=None, tag_slug=None, 
                    content_type_id=None, app_name=None, user=None, **kwargs):
    """
    A thin wrapper around ``list_detail.object_list`` which returns a
    ``QuerySet`` containing instances of TaggedItem.

    In addition to the context variables set up by ``object_list``, a
    ``tags`` context variable will contain the ``Tag`` instances.
    """
    
    tag_slug = tag_slug or kwargs.get('tag')
    tags = get_tags_from_slug(tag_slug)
    app = None
    if not queryset_or_model:
        if app_name:
            for a in settings.TAGGED_MODELS:
                if a['label'] == app_name:
                    app = a
                    app_label, model_name = app['type'].split('.')
                    break
            if app:
                content_type_id = ContentType.objects.get_by_natural_key(app_label, model_name).id
            else:
                raise Http404
        if content_type_id:
            queryset_or_model = ContentType.objects.get_for_id(content_type_id).model_class()

    queryset = TaggedItem.objects.get_by_model(queryset_or_model, tags)
    
    if not kwargs.has_key('extra_context'):
        kwargs['extra_context'] = {}
    kwargs['extra_context']['tags'] = tags
    kwargs['extra_context']['tag_slug'] = tag_slug
    kwargs['extra_context']['related_tags'] = RelatedTag.objects.get_related(tags)
    kwargs['extra_context']['app'] = app
    
    if not kwargs.has_key('template_name'):
        kwargs['template_name'] = 'tagging/taggeditem_list.html'
    
    return object_list(request, queryset, **kwargs)

def taggeditem_index(request, tag_slug, user=None, 
                     template='tagging/taggeditem_index.html'):
    tags = get_tags_from_slug(tag_slug)
    # build the content context according to the TAGGED_MODELS
    # i.e. content = {'blog': {'qs': Blog.objects.all(), 'title': 'Blog'}, ...}
    content = SortedDict()
    for app in settings.TAGGED_MODELS:
        app_label, model_name = app['type'].split('.')
        model = ContentType.objects.get_by_natural_key(app_label, model_name).model_class()
        if user:
            if hasattr(model.objects, 'filter_for_user'):
                qs = model.objects.filter_for_user(user)
            else:
                qs = model.objects.none()
        else:
            qs = model.objects.all()
        qs = TaggedItem.objects.get_by_model(qs, tags)
        content[app['label']] = {'title': app['title'], 'count': qs.count(), 'qs': qs[:10]}
    return render_to_response(template, 
                              {'tags': tags, 'tag_slug': tag_slug,
                               'related_tags': RelatedTag.objects.get_related(tags),
                               'content': content},
                              context_instance = RequestContext(request))

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


