# -*- coding: utf-8 -*-
from django import template
from django.utils.html import format_html
from itertools import chain
from main.models import *
from bs4 import BeautifulSoup as bs

register = template.Library()

def append_children(group):
    # функция осуществляет рекурсивный проход по ветке графа
    result = ''
    for child_node in group.child_nodes.all():
        result += '<li id="node_{0}" >'.format(child_node.eid) + str(child_node) + '</li>\n'
    for child_group in group.child_groups.all():
        result += '<li id="group_{0}" >'.format(child_group.eid) + str(child_group) + append_children(child_group) + '</li>\n'
    return '<ul>' + result + '</ul>'

@register.simple_tag
def build_tree(graph):
    tree = ''
    nodes = graph.contained_nodes.all()
    groups = graph.contained_groups.all()
    for root_node in nodes.filter(parent__isnull = True):
        tree += '<li id="node_{0}" >'.format(root_node.eid) + str(root_node) + '</li>\n'

    for root_group in groups.filter(parent__isnull=True):
        tree += '<li id="group_{0}" >'.format(root_group.eid) + str(root_group) + append_children(root_group) + '</li>\n'

    tree = '<ul>' + tree + '</ul>'
    tree = bs(tree)
    return tree.prettify()
