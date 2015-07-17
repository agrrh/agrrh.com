#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'agrrh'
SITENAME = 'Keep It Simple'
SITEURL = ''

PATH = 'content'
STATIC_PATHS = ['blog', 'notes', 'downloads']
ARTICLE_PATHS = ['blog', 'notes']
ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'
ARTICLE_URL = '{date:%Y}/{slug}.html'

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = 'en'

THEME = './pelican-bootstrap3'
BOOTSTRAP_THEME = 'sandstone'
PYGMENTS_STYLE = 'solarizedlight'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
	('Pelican', 'http://getpelican.com/'),
)

# Social widget
SOCIAL = (
        ('VK', 'https://vk.com/agrrh'),
	('GitHub', 'https://github.com/agrrh-'),
	('BitBucket', 'https://bitbucket.org/agrrh'),
)

DEFAULT_PAGINATION = 15

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
