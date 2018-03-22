from django.conf.urls import url
from django.views.generic import TemplateView
from dashboards.views.detail.views import DetailTemplate as detail

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="calendar.html"), name='home'),
    url(r'^(?P<day>\d+)/$', view=detail.as_view(), name='detail'),
]
