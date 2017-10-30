from django.core import serializers
from .models import Lead


def xml(quan):
    objs = Lead.objects.all()[:quan]
    data = serializers.serialize("xml", objs)
    return data
