"""
Convenience module for access of custom tagging application settings,
which enforces default settings when the main settings module does not
contain the appropriate settings.
"""
from django.conf import settings

# The maximum length of a tag's name.
MAX_TAG_LENGTH = getattr(settings, 'MAX_TAG_LENGTH', 50)

# Whether to force all tags to lowercase before they are saved to the
# database.
FORCE_LOWERCASE_TAGS = getattr(settings, 'FORCE_LOWERCASE_TAGS', True)

MAX_TAG_COUNT = getattr(settings, 'MAX_TAG_COUNT', 10)

# list of applications that tag_index view will display
if hasattr(settings, 'TAGGED_MODELS'):
    TAGGED_MODELS = getattr(settings, 'TAGGED_MODELS')
else:
    # TODO: fetch all tagged content_types from TaggedItem and build a default dict 
    pass


