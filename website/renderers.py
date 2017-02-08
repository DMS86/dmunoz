from django_medusa.renderers import StaticSiteRenderer
from django.core.urlresolvers import reverse

class HomeRenderer(StaticSiteRenderer):
    def get_paths(self):
        return frozenset([
            "/",
            "/escala-de-notas/",
        ])

renderers = [HomeRenderer, ]