from django.views.generic import TemplateView
from datetime import datetime as dt


class DetailTemplate(TemplateView):
    template_name = "detail.html"

    def index(self, **kwargs):
        day = kwargs['day']
        context = super().get_context_data(**kwargs)
        context["date"] = dt.strptime(day, '%Y-%m-%d')
        return context
