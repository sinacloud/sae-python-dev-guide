#!/usr/bin/env python

# Copyright (C) 2012-2013 SINA, All rights reserved.

"""Command line client for SAE MySQL Service. """

import sys
import os
import logging
import optparse

import sae._restful_mysql
import sae._restful_mysql._mysql_exceptions
sys.modules['_mysql_exceptions'] = sae._restful_mysql._mysql_exceptions

from grizzled import db
from grizzled.db import mysql
import prettytable
import sqlcmd
from sqlcmd import config

logging.basicConfig(level=logging.WARNING)
sqlcmd.log = logging.getLogger('cloudsql')

sqlcmd.DEFAULT_CONFIG_DIR = os.path.expanduser('~/.saecloud')
sqlcmd.RC_FILE = os.path.join(sqlcmd.DEFAULT_CONFIG_DIR, 'cloudsql.config')
sqlcmd.HISTORY_FILE_FORMAT = os.path.join(sqlcmd.DEFAULT_CONFIG_DIR, '%s.hist')
sqlcmd.INTRO = 'SAE MySQL Client\n\nType "help" or "?" for help.\n'

DEFAULT_ENCODING = 'utf-8'
USAGE = '%prog [options] database_name'

DEFAULT_SAE_MYSQL_HOST = 'w.rdc.sae.sina.com.cn'
DEFAULT_SAE_MYSQL_PORT = 3307
DEFAULT_SAE_MYSQL_DB_PREFIX = 'app_'

class CloudSqlDriver(mysql.MySQLDriver):
    """Grizzled DB Driver for Cloud SAE MySQL Service."""

    NAME = 'cloudsql'

    def get_import(self):
        return sae._restful_mysql

    def get_display_name(self):
        return 'Cloud SQL'

    def do_connect(self, host, port, user, password, database):
        # Fix grizzled's mysql driver which omit the port argument when connecting.
        dbi = self.get_import()
        port = port and int(port) or 3306
        return dbi.connect(host=host, user=user, passwd=password, db=database, port=port)

class CloudSqlCmd(sqlcmd.SQLCmd):
    """The SQLCmd command interpreter for Cloud SQL."""

    sqlcmd.SQLCmd.MAIN_PROMPT = 'mysql> '
    sqlcmd.SQLCmd.CONTINUATION_PROMPT = '    -> '

    sqlcmd.SQLCmd.NO_SEMI_NEEDED.update(
        ['about', 'desc', 'describe', 'echo', 'exit', 'h', 'hist',
         'history', 'load', 'run', 'r', 'redo', 'set', 'show', 'var', 'vars'])

    for method in ['do_dot_connect', 'do_dot_desc', 'do_begin']:
        delattr(sqlcmd.SQLCmd, method)

    for cmd in ['show', 'describe', 'echo', 'load', 'run', 'exit', 'h',
                'hist', 'history', 'var', 'vars', 'about']:
        method = 'do_dot_' + cmd
        setattr(sqlcmd.SQLCmd, method.replace('dot_', ''), getattr(
            sqlcmd.SQLCmd, method))
        delattr(sqlcmd.SQLCmd, method)
        method = 'complete_dot_' + cmd
        if hasattr(sqlcmd.SQLCmd, method):
            setattr(sqlcmd.SQLCmd, method.replace('dot_', ''), getattr(
                sqlcmd.SQLCmd, method))
            delattr(sqlcmd.SQLCmd, method)

    def do_redo(self, args):
        # XXX: Fix global name 'do_r' is not defined problem in sqlcmd
        self.do_r(args)

    def _SQLCmd__set_setting(self, varname, value):
        # XXX: Fix bool object has no lower attribute in sqlcmd
        return sqlcmd.SQLCmd._SQLCmd__set_setting(self, varname, str(value))

    def do_desc(self, args):
        self.do_describe(args, cmd='.desc')
    complete_desc = sqlcmd.SQLCmd.complete_dot_desc

    def do_load(self, args):
        self.do_run(args)

    def preloop(self, *args, **kwargs):
        sqlcmd.SQLCmd.preloop(self, *args, **kwargs)
        # Just exit if the connect failed
        if self._SQLCmd__db is None: sys.exit(1)

    def __init__(self, *args, **kwargs):
        sqlcmd.SQLCmd.__init__(self, *args, **kwargs)
        self.prompt = sqlcmd.SQLCmd.MAIN_PROMPT
        self.output_encoding = DEFAULT_ENCODING

    def set_output_encoding(self, encoding):
        self.output_encoding = encoding

    def _build_table(self, cursor):
        """Builds an output PrettyTable from the results in the given cursor."""
        if not cursor.description:
            return None

        column_names = [column[0] for column in cursor.description]
        table = prettytable.PrettyTable(column_names)
        rows = cursor.fetchall()
        if not rows:
            return table
        for i, col in enumerate(rows[0]):
            table.align[column_names[i]] = isinstance(col, basestring) and 'l' or 'r'
        for row in rows: table.add_row(row)
        return table

    def _SQLCmd__handle_select(self, args, cursor, command='select'):
        """Overrides SQLCmd.__handle_select to display output with prettytable."""
        self._SQLCmd__exec_SQL(cursor, command, args)
        table = self._build_table(cursor)
        if table:
            output = table.get_string()
            if isinstance(output, unicode):
                print output.encode(self.output_encoding)
            else:
                print output

def _create_config_dir():
    """Creates the sqlcmd config directory if necessary."""
    directory = sqlcmd.DEFAULT_CONFIG_DIR
    if not os.access(directory, os.R_OK | os.W_OK | os.X_OK):
        old_umask = os.umask(077)
        os.makedirs(sqlcmd.DEFAULT_CONFIG_DIR)
        os.umask(old_umask)

def main(argv):
    parser = optparse.OptionParser(usage=USAGE)
    parser.add_option('-u', '--username', dest='username',
                      help='MySQL username to use when connecting to the server.')
    parser.add_option('-p', '--password', dest='password',
                      help='MySQL password to use when connecting to the server.')
    parser.add_option('-e', '--output_encoding', dest='output_encoding',
                      default=DEFAULT_ENCODING,
                      help='Output encoding. Defaults to %s.' % DEFAULT_ENCODING)

    (options, args) = parser.parse_args(argv[1:])

    if len(args) != 1:
        parser.print_help(sys.stderr)
        return 1

    if not options.username or not options.password:
        print >>sys.stderr, 'Error: username or password is missing.\n'
        return 1

    if args[0].startswith(DEFAULT_SAE_MYSQL_DB_PREFIX):
        database_name = args[0]
    else:
        database_name = DEFAULT_SAE_MYSQL_DB_PREFIX + args[0]
    instance_alias = database_name

    _create_config_dir()

    db.add_driver(CloudSqlDriver.NAME, CloudSqlDriver)
    sql_cmd_config = config.SQLCmdConfig(None)
    sql_cmd_config.add('__cloudsql__', instance_alias,
                       DEFAULT_SAE_MYSQL_HOST , DEFAULT_SAE_MYSQL_PORT, database_name,
                       CloudSqlDriver.NAME, options.username, options.password)
    sql_cmd = CloudSqlCmd(sql_cmd_config)
    sql_cmd.set_output_encoding(options.output_encoding)
    sql_cmd.set_database(instance_alias)
    sql_cmd.cmdloop()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
