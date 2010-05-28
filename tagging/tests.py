__test__ = {"doctest": """

>>> from tagging.models import *
>>> from tagging.utils import *
>>> a=Tag.objects.create(name='a')
>>> b=Tag.objects.create(name='b')

Related tag tests
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

Usage count test
>>> Tag.objects.add_tag(a, 'b')
>>> get_tag('b').usage
1
>>> Tag.objects.add_tag(a, 'b')
>>> get_tag('b').usage
1
>>> ti = TaggedItem.objects.get(tag=get_tag('b'))
>>> ti.delete()
>>> get_tag('b').usage
0
"""}

