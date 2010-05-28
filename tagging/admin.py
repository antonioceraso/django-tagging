from django.contrib import admin
from tagging.models import Tag, TaggedItem, RelatedTag
from tagging.forms import TagAdminForm

class TagAdmin(admin.ModelAdmin):
    form = TagAdminForm
    list_display = ('name', 'slug', 'added', 'last', 'is_valid', 'usage')
    list_filter = ('is_valid',)
    list_editable = ('is_valid',)
    search_fields = ('name',)
admin.site.register(Tag, TagAdmin)

class RelatedTagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'relation_type', 'related_tag', 'added', 'count')
    list_filter = ('relation_type',)
    list_editable = ('relation_type',)
    search_fields = ('tag__name', 'related_tag__name')
    
    def get_actions(self, request):
        # do not let deletion of relations, instead set relation_type to '!'
        actions = super(RelatedTagAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
admin.site.register(RelatedTag, RelatedTagAdmin)

class TaggedItemAdmin(admin.ModelAdmin):
    list_display = ('tag', 'object', 'added')
    search_fields = ('tag',)
admin.site.register(TaggedItem, TaggedItemAdmin)

