from django.views.generic import TemplateView


class DetailTemplate(TemplateView):
    template_name = "detail.html"

    def index(self, **kwargs):
        day = kwargs['day']
        context = super().get_context_data(**kwargs)
        context["day"] = "day"
        return context
