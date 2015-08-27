from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns("",
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^escala-de-notas/$", TemplateView.as_view(template_name="escala.html"), name="escala"),
)