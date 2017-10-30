from django.conf.urls import url
from . import views

app_name = 'objects'

urlpatterns = [
    url(r'^leads/(?P<size>[0-9]+)/$', views.leads, name='leads')
]
