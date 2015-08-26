from django_medusa.renderers import StaticSiteRenderer
from zinnia.models import Entry
from django.core.urlresolvers import reverse


class EntriesRenderer(StaticSiteRenderer):
    def get_paths(self):
        # A "set" so we can throw items in blindly and be guaranteed that
        # we don't end up with dupes.
        paths = set(["/blog/", ])

        items = Entry.published.all().order_by('-creation_date')
        for item in items:
            paths.add(item.get_absolute_url())

        # Cast back to a list since that's what we're expecting.
        return list(paths)

class HomeRenderer(StaticSiteRenderer):
    def get_paths(self):
        return frozenset([
            "/",
            "/blog/",
            "/escala-de-notas/",
        ])

renderers = [HomeRenderer, EntriesRenderer, ]