"""Constants about app

"""
import os
import conf

# Private
APP_NAME = os.environ.get('APP_NAME', '')
APP_HASH = os.environ.get('APP_HASH', '')
ACCESS_KEY = os.environ.get('ACCESS_KEY', '')
SECRET_KEY = os.environ.get('SECRET_KEY', '')

# Public
MYSQL_DB = '_'.join(['app', APP_NAME])
MYSQL_USER = ACCESS_KEY
MYSQL_PASS = SECRET_KEY
MYSQL_HOST = conf.SAE_MYSQL_HOST_M
MYSQL_PORT = conf.SAE_MYSQL_PORT
MYSQL_HOST_S = conf.SAE_MYSQL_HOST_S
