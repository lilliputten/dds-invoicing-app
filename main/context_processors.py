# -*- coding:utf-8 -*-
import os
import posixpath
import re
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from pprint import pprint

# from django.shortcuts import render
from django.template import Context, Template

import logging
LOG = logging.getLogger(__name__)

# ATTENTION: dynamic creation of the assets list, see routines below // 2015.10.23
# _blocks_files_scan = False
_blocks_files_cache_timeout = None  # 15*60 # seconds: {min}*60
_blocks_files_processed = False
_blocks_files = {}
_blocks_files_extensions = [
    'less',
    'coffee',
]
_blocks_files_templates = {
    'less': '!template__blocks_less.less',
    'coffee': '!template__blocks_coffee.include',
}
# _blocks_files_templates_to_result_re = re.compile(r'\.(django|template)$')
_blocks_files_templates_to_result_re = re.compile(r'!(django|template)[\._-]')


def _process_blocks_files():

    global _blocks_files_processed
    global _blocks_files

    msg = u'Loading block files list from %s' % settings.BLOCKS_ROOT
    LOG.info(msg)
    print(msg)
    for ext in _blocks_files_extensions:
        _blocks_files[ext] = []
    for root, dirs, files in os.walk(settings.BLOCKS_ROOT):
        dir = root[len(settings.STATIC_ROOT):]
        # print 'root: %s dir: %s' % ( root, dir )
        for fname in files:
            file = posixpath.join(dir, fname)
            # print('\t%s' % ( file ) )
            for ext in _blocks_files_extensions:
                if file.endswith('.' + ext):
                    _blocks_files[ext].append(file)
                    # print('\t[%s] %s' % ( ext, file ) )

    for ext in _blocks_files_templates.keys():
        template_file = _blocks_files_templates[ext]
        result_file = _blocks_files_templates_to_result_re.sub('', template_file)
        print(u'Make from template: %s --> %s' % (template_file, result_file))
        if os.path.isfile(posixpath.join(settings.STATIC_ROOT, template_file)):
            with open(posixpath.join(settings.STATIC_ROOT, template_file), 'rb') as th:
                s = Template(th.read()).render(Context({
                    'settings': settings.PASS_VARIABLES,
                    'files': _blocks_files[ext],
                }))
                with open(posixpath.join(settings.STATIC_ROOT, result_file), 'wb') as f:
                    f.write(s.encode())

    _blocks_files_processed = True


def _get_blocks_files(ext):

    global _blocks_files_processed
    global _blocks_files

    if not _blocks_files_processed:
        _process_blocks_files()

    return _blocks_files[ext]


def common_values(request):

    current_site = get_current_site(request)

    fetch_attr = (
        'GOOGLE_ANALYTICS_PROPERTY_ID',
        'GOOGLE_SITE_VERIFICATION_ID',
    )

    data = {}

    for id in fetch_attr:
        attr = getattr(settings, id, False)
        if not settings.LOCAL and not settings.DEBUG and attr:
            data[id] = attr

    data['settings'] = settings.PASS_VARIABLES
    data['site'] = 'http://%s' % current_site.domain

    # ATTENTION: dynamic creation of the assets list
    if settings.BLOCKS_FILES_SCAN:
        for ext in _blocks_files_extensions:
            key = 'block_files_' + ext
            result = cache.get(key)
            if result is None:
                result = _get_blocks_files(ext)
                cache.set(key, result, _blocks_files_cache_timeout)
            data[key] = result

    return data
