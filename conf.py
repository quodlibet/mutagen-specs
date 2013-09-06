# -*- coding: utf-8 -*-

import sys, os

source_suffix = '.rst'
master_doc = 'index'
project = u'Mutagen Specs'
version = '1.0'
release = '1.0'
pygments_style = 'tango'
html_theme_path = ['.']
html_theme = 'flask'

sys.path.append(os.path.abspath('exts'))

extensions = ['numfig']
