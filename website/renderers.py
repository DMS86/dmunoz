from django_medusa.renderers import StaticSiteRenderer

class HomeRenderer(StaticSiteRenderer):
    def get_paths(self):
        return frozenset([
            "/",
            "/blog/",
            "/escala-de-notas/",
        ])

renderers = [HomeRenderer, ]