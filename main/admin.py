from django.contrib import admin
from .models import *

admin.site.register(Group)
admin.site.register(Node)
admin.site.register(ParentItem)
admin.site.register(Graph)

