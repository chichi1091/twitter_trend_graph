from django.conf.urls import url
from django.views.generic import TemplateView
from dashboards.views.views import TrendsView
from dashboards.views.detail.views import TrendsDetailView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="calendar.html"), name='home'),
    url(r'^(?P<day>\d+)/$', TemplateView.as_view(template_name="detail.html"), name='detail'),

    url(r'^api/trends/$', view=TrendsView.as_view()),
    url(r'^api/trends/(?P<day>\d+)$', view=TrendsDetailView.as_view()),
]
