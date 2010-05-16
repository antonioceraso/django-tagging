__test__ = {"doctest": """

Related tag tests
>>> from tags.models import Tag, RelatedTag
>>> t1 = Tag.objects.create(name='t1')
>>> t2 = Tag.objects.create(name='t2')
>>> t3 = Tag.objects.create(name='t3')
>>> t4 = Tag.objects.create(name='t4')
>>> RelatedTag.objects.relate([t1, t2, t3])
>>> t1.get_related()
[<Tag: t2>, <Tag: t3>]
>>> t2.get_related()
[<Tag: t1>, <Tag: t3>]
>>> t3.get_related()
[<Tag: t1>, <Tag: t2>]
>>> related_tag = RelatedTag.objects.get(tag=t1, related_tag=t2)
>>> related_tag.related = False
>>> related_tag.save()
>>> symm = RelatedTag.objects.get(tag=t2, related_tag=t1)
>>> symm.related
False
>>> t1.get_related()
[<Tag: t3>]
# testing relate with deep=True
>>> RelatedTag.objects.relate([t1, t4], depth=1)
>>> t4.get_related()
[<Tag: t1>, <Tag: t3>]
>>> t3.get_related()
[<Tag: t1>, <Tag: t2>, <Tag: t4>]

"""}

