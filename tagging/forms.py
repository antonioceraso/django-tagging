from django import forms
from django.utils.translation import ugettext as _
from tagging import settings
from tagging.models import Tag
from tagging.utils import parse_tag_input

class TagAdminForm(forms.ModelForm):
    class Meta:
        model = Tag

    def clean_name(self):
        value = self.cleaned_data['name']
        tag_names = parse_tag_input(value)
        if len(tag_names) > 1:
            raise forms.ValidationError(_('Multiple tags were given.'))
        elif len(tag_names[0]) > settings.MAX_TAG_LENGTH:
            raise forms.ValidationError(
                _('A tag may be no more than %s characters long.') %
                    settings.MAX_TAG_LENGTH)
        return value


class TagField(forms.CharField):
    """
    A ``CharField`` which validates that its input is a valid list of
    tag names.
    """
    def __init__(self, *args, **kwargs):
        self.widget = forms.TextInput(attrs={'class':'tag_field'})
        super(TagField, self).__init__(*args, **kwargs)
