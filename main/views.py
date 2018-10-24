from django.shortcuts import render, reverse, HttpResponseRedirect, Http404
from .forms import UploadGraphForm
from .models import *
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs

def index(request):
    form = UploadGraphForm()
    return render(request, 'index.html', {'form': form})

def graph_list(request):
    return render(request, 'graph_list.html', {'graph_list': Graph.objects.all()})

def create_graph(request):
    if request.method == 'POST':
        # parsing a text file into bs object
        file = request.FILES['graph']
        file_contents = file.read().decode(encoding="utf-8").replace('“', '"').replace('”', '"')
        document = bs(file_contents, 'lxml')
        graph = Graph.objects.create()
        # creating nodes, assigning them to new graph
        for node in document.find_all(['node']):
            new_node = Node()
            new_node.eid = node['eid']
            new_node.text = node.text
            new_node.save()
            graph.contained_nodes.add(new_node)
        # doing same for groups
        for group in document.find_all(['group']):
            new_group = Group()
            new_group.eid = group['eid']
            new_group.text = group.text
            new_group.save()
            graph.contained_groups.add(new_group)
            # print(group['groupped'].split())
        graph.save()
        # building hierarchy
        for group in document.find_all(['group']):
            group_obj = Group.objects.get(graph = graph, eid=group['eid'])
            for child_id in group['groupped'].split():
                try:
                    child = Node.objects.get(graph=graph, eid=child_id)
                except ObjectDoesNotExist:
                    child = Group.objects.get(graph=graph, eid=child_id)
                child.parent = group_obj
                child.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return Http404