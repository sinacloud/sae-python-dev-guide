
import os.path
from setuptools import setup, find_packages

VERSION = '1.2.0'

scripts = ['dev_server.py', 'saecloud', 'cloudsql.py']

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
        # XXX: The latest grizzled-python package is broken
        'grizzled-python==1.0.1',
        'sqlcmd',
        'prettytable',
        ],
    platforms='any',
    url = "http://python.sinaapp.com",
    packages=find_packages(),
    scripts = scripts,
    zip_safe = False,
)
