__test__ = {"doctest": """

Related tag tests
>>> from tagging.models import *
>>> from tagging.utils import *
>>> a=Tag.objects.create(name='a')
>>> b=Tag.objects.create(name='b')
>>> RelatedTag.objects.relate_all('a, b')
>>> RelatedTag.objects.all()
[<RelatedTag: a ~ b>, <RelatedTag: b ~ a>]
>>> RelatedTag.objects.relate('a', '>', 'b')
>>> RelatedTag.objects.all()
[<RelatedTag: a > b>, <RelatedTag: b < a>]
>>> RelatedTag.objects.relate('a', '.', 'b')
>>> RelatedTag.objects.all()
[<RelatedTag: a . b>, <RelatedTag: b _ a>]
>>> RelatedTag.objects.relate('a', '~', 'b')
>>> RelatedTag.objects.all()
[<RelatedTag: a ~ b>, <RelatedTag: b ~ a>]
"""}

