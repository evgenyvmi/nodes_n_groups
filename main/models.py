from django.db.models import *
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class ParentItem(Model):
    content_type = ForeignKey(ContentType, verbose_name='parent type', related_name='parent_group', on_delete=DO_NOTHING)
    parent_id = PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'parent_id')

    def __unicode__(self):
        return self.content_type.name + ' ' + self.parent_id

class Group(Model):
    text = CharField(verbose_name=u'text', max_length=50)
    eid = PositiveIntegerField()
    parent = ForeignKey(ParentItem,
                        verbose_name='parent objects',
                        related_name='group_children',
                        null=True, blank=True,
                        on_delete=CASCADE)
    def __unicode__(self):
        return self.text

    # @property
    # def parent_id(self):
    #     try:
    #         parent = ParentItem.objects.get(parent_id=self.eid)
    #         return parent.id
    #     except:
    #         return None

class Node(Model):
    text = CharField(verbose_name=u'text', max_length=50)
    eid = PositiveIntegerField()
    parent = ForeignKey(ParentItem,
                        verbose_name='parent objects',
                        related_name='node_children',
                        null=True, blank=True,
                        on_delete=CASCADE)
    def __unicode__(self):
        return self.text

    # @property
    # def parent_id(self):
    #     try:
    #         parent = ParentItem.objects.get(parent_id=self.eid)
    #         return parent.id
    #     except:
    #         return None

class Graph(Model):
    structure = TextField(verbose_name=u'graph structure', max_length=1000)
    contained_nodes = ManyToManyField(Node)
    contained_groups = ManyToManyField(Group)
