#-*-coding: utf8 -*-

import os.path
root = os.path.dirname(__file__)

import sys
sys.path.insert(0, os.path.join(root, 'site-packages'))

os.environ['TRAC_ENV'] = os.path.join(root, 'project')
#os.environ['TRAC_ENV_PARENT_DIR'] = os.path.join(root, 'projects')

import trac.web.main as main
application = main.dispatch_request
