
import os.path
from setuptools import setup

VERSION = '1.0.3'

scripts = ['dev_server.py', 'saecloud']

if os.name == 'nt':
    # XXX: shebang does not work on windows
    BAT = 'saecloud.bat'
    f = os.path.join(os.path.dirname(__file__), BAT)
    open(f, 'w').write('@python "%~dp0\saecloud" %*')
    scripts.append(BAT)

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
