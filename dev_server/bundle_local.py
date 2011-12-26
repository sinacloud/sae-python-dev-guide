#!/usr/bin/env python

"""Create a local bundle for your virtualenv environment

Export all the packages listed in requirements.txt to ./virtualenv.bundle
directory

Then you can create a .zip file before uploading them to sae

Usage: bundle_local -r requirements.txt

"""

from optparse import OptionParser
import os
import sys
import pip.util
import shutil

TMP = 'virtualenv.bundle'

ZIP_FILE = TMP + '.zip'

def main():
    parser = OptionParser()
    parser.add_option("-r", dest="requirements",
                      help="The requirements.txt file outputed by pip freeze")
    (options, args) = parser.parse_args()

    if not options.requirements:
        print 'requirements.txt not found'
        sys.exit(-1)

    if os.path.exists(TMP):
        shutil.rmtree(TMP)
    os.mkdir(TMP)

    shutil.copy2(options.requirements, os.path.join(TMP, 'requirements.txt'))

    # Get all installed packages on system
    installed_dists = {}
    for dist in pip.util.get_installed_distributions():
        installed_dists[dist.project_name] = dist

    # Get the dists in requirements.txt
    dists = []
    for line in open(options.requirements, 'r').readlines():
        if line.strip() or line.startswith('#'):
            pass
        pkg = line.split('==')[0]

        if pkg not in installed_dists:
            raise Exception('%s not installed' % pkg)
        dists.append(installed_dists[pkg])

    top_levels = []
    for dist in dists:
        mods = [os.path.join(dist.location, mod) for mod in dist.get_metadata('top_level.txt').splitlines()]
        top_levels += mods

    top_levels = list(set(top_levels))
    copy_modules(top_levels, TMP)


def copy_modules(mod_paths, dest):
    for mod in mod_paths:
        if os.path.isdir(mod):
            shutil.copytree(mod, os.path.join(dest, os.path.basename(mod)), ignore=shutil.ignore_patterns('*.pyc'))
        else:
            # Single file module
            shutil.copy2(mod + '.py', dest)

if __name__ == '__main__':
    main()
