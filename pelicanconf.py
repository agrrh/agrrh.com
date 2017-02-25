#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'agrrh'
SITENAME = 'Keep It Simple, Sir!'
SITEURL = ''

PATH = './'
STATIC_PATHS = ['pages', 'downloads', 'media']
ARTICLE_PATHS = ['personal', 'technical', 'projects']
ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'
ARTICLE_URL = '{date:%Y}/{slug}.html'

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = 'en'

THEME = './themes/pelican-bootstrap3'
BOOTSTRAP_THEME = 'yeti'
PYGMENTS_STYLE = 'solarizedlight'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
DISPLAY_TAGS_ON_SIDEBAR = True

DISQUS_SITENAME = 'agrrh-com'
DISQUS_PUBLIC_KEY = 'dgDf7227PBnxTTjAJtFRh9EUVQPSuNHosQFlwRjvZA2YQ23wbmXtNlLqnl5Wg3f0'
DISQUS_SECRET_KEY = str(open('./.disqus_api_secret', 'r').read()).strip()

TAG_CLOUD_MAX_ITEMS = 10
DISPLAY_TAGS_INLINE = True
TAGS_URL = 'tags.html'

PLUGIN_PATHS = ["./plugins"]
PLUGINS = ['tag_cloud', 'i18n_subsites', 'disqus_static']

# Blogroll
LINKS = (
    ('Pelican', 'http://getpelican.com/'),
)

# Social widget
SOCIAL = (
    ('VK', 'https://vk.com/agrrh'),
    ('GitHub', 'https://github.com/agrrh'),
)

DEFAULT_PAGINATION = 15

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# https://github.com/getpelican/pelican-themes/issues/460
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}

