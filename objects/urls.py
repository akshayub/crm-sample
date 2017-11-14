from django.conf.urls import url
from . import views

app_name = 'objects'

urlpatterns = [
    url(r'^xml/leads/(?P<size>[0-9]+)/$', views.leads_xml, name='leads_xml'),
    url(r'^json/leads/(?P<size>[0-9]+)/$', views.leads_json, name='leads_json'),
    url(r'^accounts/(?P<dtype>[a-z]+)/(?P<start>[0-9]+)/(?P<end>[0-9]+)/$', views.accounts, name='accounts'),
    url(r'^contacts/(?P<dtype>[a-z]+)/(?P<start>[0-9]+)/(?P<end>[0-9]+)/$', views.contacts, name='contacts'),
    url(r'^leads/(?P<dtype>[a-z]+)/(?P<start>[0-9]+)/(?P<end>[0-9]+)/$', views.leads, name='leads'),
    url(r'^update_lead/(?P<lid>[0-9]+)/(?P<status>[0-9]+)/$', views.update_lead, name='update_lead'),
    url(r'^opportunities/(?P<dtype>[a-z]+)/(?P<start>[0-9]+)/(?P<end>[0-9]+)/$', views.opportunities, name='opportunities'),
    url(r'^update_oppo/(?P<oid>[0-9]+)/(?P<stage>[0-9]+)/$', views.update_oppo, name='update_opportunity'),
    url(r'^del_acc/(?P<aid>[0-9]+)/$', views.account_delete, name='del_acc'),
    url(r'^del_ctc/(?P<cid>[0-9]+)/$', views.contact_delete, name='del_ctc'),
    url(r'^del_lead/(?P<lid>[0-9]+)/$', views.lead_delete, name='del_lead'),
    url(r'^del_oppo/(?P<oid>[0-9]+)/$', views.oppo_delete, name='del_oppo'),
    url(r'^sch_acc/$', views.account_search, name='sch_acc'),
    url(r'^sch_ctc/$', views.contact_search, name='sch_ctc'),
    url(r'^sch_lead/$', views.lead_search, name='sch_lead'),
    url(r'^sch_oppo/$', views.oppo_search, name='sch_oppo'),
    url(r'^lead_db/$', views.dashboard_lead_data, name='lead_db'),
    url(r'^oppo_db/$', views.dashboard_oppo_data, name='oppo_db'),
    url(r'^recent_leads/$', views.recent_unclosed_leads, name='recent_leads')
]
