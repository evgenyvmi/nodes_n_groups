# -*- coding: utf-8 -*-
from django import template
from itertools import chain
from main.models import *

register = template.Library()

def append_children(group):
    # функция осуществляет рекурсивный проход по ветке графа
    result = ''
    for child_node in group.child_nodes.all():
        result += '<li id="node_{0}" >'.format(child_node.eid) + str(child_node) + '</li>'
    for child_group in group.child_groups.all():
        result += '<li id="node_{0}" >'.format(child_group.eid) + str(child_group) + append_children(child_group) + '</li>'
    return '<ul>' + result + '</ul>'

@register.simple_tag
def build_structure(graph):
    graph_list = ''
    nodes = graph.contained_nodes.all()
    groups = graph.contained_groups.all()
    for root_node in nodes.filter(parent__isnull = True):
        graph_list += '<li id="node_{0}" >'.format(root_node.eid) + str(root_node) + '</li>'
        print(root_node.eid)

    for root_group in groups.filter(parent__isnull=True):
        graph_list += '<li id="group_{0}" >'.format(root_group.eid) + str(root_group) + append_children(root_group) + '</li>'

        print(root_group.eid)
        
    return '<ul>' + graph_list + '</ul>'
