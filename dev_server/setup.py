
from setuptools import setup

scripts = ['dev_server.py', 'saecloud']

import os
if os.name == 'nt':
    scripts.append('saecloud.bat')

setup(
    name = "sae-python-dev",
    version = "1.0testing",
    author = "Jaime Chen",
    author_email = "chenzheng2@staff.sina.com.cn",
    description = ("SAE Python development server"),
    install_requires = [
        'Werkzeug',
        'pip',
        'PyYAML',
        'argparse',
        ],
    platforms='any',
    license = "",
    url = "http://appstack.sinaapp.com",
    packages=['sae'],
    scripts = scripts
)
