#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'agrrh'
SITENAME = 'Keep It Simple, Sir!'
SITEURL = 'https://agrrh.com'

THEME = './themes/pelican-bootstrap3'
BOOTSTRAP_THEME = 'yeti'
PYGMENTS_STYLE = 'solarizedlight'

CUSTOM_CSS = 'static/custom.css'
CUSTOM_JS = 'static/custom.js'

PATH = './'
STATIC_PATHS = [
    'pages',
    'downloads',
    'media',
    'extra',
    'errors'
]
EXTRA_PATH_METADATA = {'extra/favicon.ico': {'path': 'favicon.ico'},
                       'extra/custom.css': {'path': 'static/custom.css'},
                       'extra/custom.js': {'path': 'static/custom.js'}}

ARTICLE_PATHS = [
    'contents',
]

ARTICLE_URL = '{date:%Y}/{slug}'
ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'
PAGE_URL = 'pages/{slug}'
PAGE_SAVE_AS = 'pages/{slug}.html'
CATEGORY_URL = 'category/{slug}'
CATEGORY_SAVE_AS = 'category/{slug}.html'
TAG_URL = 'tag/{slug}'
TAG_SAVE_AS = 'tag/{slug}.html'

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss'
FEED_MAX_ITEMS = 20

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True

DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_CATEGORIES_ON_SIDEBAR = False
DISPLAY_ARCHIVE_ON_SIDEBAR = True

DISQUS_SITENAME = 'agrrh-com'

TAG_CLOUD_MAX_ITEMS = 10
DISPLAY_TAGS_INLINE = False
TAGS_URL = 'tags.html'

PLUGIN_PATHS = ["./plugins"]
PLUGINS = [
    'tag_cloud',
    'i18n_subsites'
]

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.tables': {},
        'mdx_video': {}
    },
    'output_format': 'html5'
}

# Blogroll
LINKS = (
    ('Pelican', 'http://getpelican.com/'),
    ('Caddy', 'https://caddyserver.com/')
)

# Social widget
SOCIAL = (
    ('vk', 'https://vk.com/agrrh'),
    ('github', 'https://github.com/agrrh'),
)

DEFAULT_PAGINATION = 15

# Analytics
PIWIK_URL = 'piwik.agrrh.com'
PIWIK_SITE_ID = 1

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

# https://github.com/getpelican/pelican-themes/issues/460
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}

DELETE_OUTPUT_DIRECTORY = False
