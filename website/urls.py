from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^escala-de-notas/$", TemplateView.as_view(template_name="escala.html"), name="escala"),
    url(r'^blog/', include('zinnia.urls', namespace='zinnia')),
	url(r'^comments/', include('django_comments.urls')),
    url(r'^admin/', include(admin.site.urls)),
)