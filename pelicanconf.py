#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Diego Mu\xf1oz'
SITENAME = u'Diego Mu\xf1oz Sáez'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Santiago'

DEFAULT_LANG = u'es-CL'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (('Google Scholar', 'http://scholar.google.cl/citations?user=kpxPKhQAAAAJ&hl=en'),
         ('ResearchGate', 'https://www.researchgate.net/profile/Diego_Munoz_Saez'),
         ('LinkedIn', 'https://www.linkedin.com/profile/view?id=174080633'),)

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ["images", "extras/CNAME"]
EXTRA_PATH_METADATA = {'extras/CNAME': {'path': 'CNAME'}, }

THEME = './themes/custom-zurb-F5-basic'
PLUGIN_PATHS = ['home/diego/pelican/plugins']

PLUGINS = [
'pelican_gist',
]