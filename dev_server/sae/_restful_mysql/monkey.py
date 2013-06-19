
# Copyright (C) 2012-2013 SINA, All rights reserved.

def patch():
    import sys

    if  'MySQLdb' in sys.modules:
        import warnings
        warnings.warn('MySQLdb has alreay been imported', Warning)

    modules_to_replace = (
        'MySQLdb',
        'MySQLdb.release',
        'MySQLdb.connections',
        'MySQLdb.cursors',
        'MySQLdb.converters',
        'MySQLdb.constants',
        'MySQLdb.constants.CLIENT',
        'MySQLdb.constants.FIELD_TYPE',
        'MySQLdb.constants.FLAG',
    )

    for name in modules_to_replace:
        if name in sys.modules:
            sys.modules.pop(name)

    import sae._restful_mysql
    from sae._restful_mysql import _mysql, _mysql_exceptions
    sys.modules['MySQLdb'] = sae._restful_mysql
    sys.modules['_mysql'] = _mysql
    sys.modules['_mysql_exceptions'] = _mysql_exceptions
