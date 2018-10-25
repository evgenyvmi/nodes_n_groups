from django.db.models import *
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Group(Model):
    text = CharField(verbose_name=u'text', max_length=50)
    eid = PositiveIntegerField()
    parent = ForeignKey('self',
                        verbose_name='parent objects',
                        related_name='child_groups',
                        null=True, blank=True,
                        on_delete=CASCADE)
    def __str__(self):
        return 'Group' + str(self.eid)

class Node(Model):
    text = CharField(verbose_name=u'text', max_length=50)
    eid = PositiveIntegerField()
    parent = ForeignKey(Group,
                        verbose_name='parent objects',
                        related_name='child_nodes',
                        null=True, blank=True,
                        on_delete=CASCADE)
    def __str__(self):
        return 'Node' + str(self.eid)

class Graph(Model):
    structure = TextField(verbose_name=u'graph structure', max_length=1000, null=True, blank=True)
    contained_nodes = ManyToManyField(Node, related_name='graph')
    contained_groups = ManyToManyField(Group, related_name='graph')
