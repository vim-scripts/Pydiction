#!/usr/bin/env python
# pydiction.py 0.5


""" pydiction creats a dictionary of Python module attributes for vim's completion feature.
    Usage: pydiction.py <module(s)> [-v]
    (Note: If you're getting import errors try importing the Package's main module below in this file)

    Example: The following will append all the time and math modules' attributes to the file "pydiction" with 
             and without the "time." and "math." prefix:   
             
                 $python pydiction.py time math
             
             To print the output to stdout, supply the -v option (This won't append to the pydiction file):
             
                 $python pydiction.py -v time math
"""
             


__author__ = 'Ryan (gt3) Kulla <ambiod@sbcglobal.net>'
__version__ = '0.5'


import os
import sys
import types


def main_loop(write_to):
    sub_mods = []

    for mod_name in sys.argv[1:]:
        sub_mods = mod_lookup(mod_name, sub_mods, write_to)

        # process current mod_name's submodules
        for mod_name in sub_mods:
            sub_mods = mod_lookup(mod_name, sub_mods, write_to, False)


def mod_lookup(mod_name, sub_mods, write_to, dig=True):
    prefix_on = {True:"%s.%s(", False:"%s.%s"}
    prefix_off = {True:"%s(", False:"%s"}

    try:
        exec "import %s" % mod_name
    except ImportError, err_msg:
        if sub_mods != []: # sub_mod isn't an importable module
            sub_mods.remove(mod_name) 
        else: 
            sys.stderr.write("ImportError: %s\n" % err_msg)
            sys.exit()

    mod_contents = dir(eval(mod_name))

    write_to.write('\n-- %(x)s module with "%(x)s." prefix --\n' % {'x': mod_name})
    for attr in mod_contents:
        if callable(getattr(eval(mod_name), attr)):
            write_to.write(prefix_on[True] % (mod_name, attr) + '\n')
        else:
            write_to.write(prefix_on[False] % (mod_name, attr) + '\n')
            if dig is True: # dig for submodules
                if type(getattr(eval(mod_name), attr)) is types.ModuleType:
                    sub_mods.append(mod_name + '.' + attr)

    write_to.write('\n-- %(x)s module without "%(x)s." prefix --\n' % {'x': mod_name})
    for attr in mod_contents:
        if callable(getattr(eval(mod_name), attr)):
            write_to.write(prefix_off[True] % attr + '\n')
        else:
            write_to.write(prefix_off[False] % attr + '\n')

    return sub_mods


if __name__ == '__main__':
    if sys.version_info[0:2] < (2, 3):
        sys.stderr.write("Please upgrade to Python 2.3 or greater\n")
        sys.exit()

    if len(sys.argv) <= 1:
        sys.stderr.write("%s requires at least one argument\n" % sys.argv[0])
        sys.exit()

    if "-v" in sys.argv:
        write_to = sys.stdout
        sys.argv.remove("-v")
    else:
        if os.path.exists("pydiction"):
            print "Appending to pydiction file.."
        else:
            print "Creating and writing to pydiction file.."
        write_to = open("pydiction", "a")

    main_loop(write_to)
