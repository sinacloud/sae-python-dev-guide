
from setuptools import setup

VERSION = '1.0.2'

scripts = ['dev_server.py', 'saecloud']

import os
if os.name == 'nt':
    scripts.append('saecloud.bat')

setup(
    name = 'sae-python-dev',
    version = VERSION,
    author = 'SAE Python Team',
    author_email = 'saemail@sina.cn',
    description = ('SAE Python development server'),
    install_requires = [
        'Werkzeug',
        'pip',
        'PyYAML',
        'argparse',
        ],
    platforms='any',
    url = "http://python.sinaapp.com",
    packages=['sae'],
    scripts = scripts
)
