from django.conf.urls import url
from . import views

app_name = 'web'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^compare/$', views.compare, name='compare'),
    url(r'^accounts/$', views.accounts, name='accounts'),
    url(r'^accounts/(?P<aid>[0-9]+)/$', views.account, name='account'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^contacts/(?P<cid>[0-9]+)/$', views.contact, name='contact'),
    url(r'^leads/$', views.leads, name='leads'),
    url(r'^opportunities/$', views.opportunities, name='opportunities'),
    url(r'^chart1/$', views.chart1, name='chart1'),
    url(r'^chart2/$', views.chart2, name='chart2'),
    url(r'^chart3/$', views.chart3, name='chart3')
]
