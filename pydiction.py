#!/usr/bin/env python
# pydiction.py 
# Author: Ryan (gt3) Kulla  <ambiod@sbcglobal.net>
# Version: 0.2
# Date: Dec 2003
# Desc: Used for creating a dictionary of Python's module/method names for vim's completion feature.
# Usage: pydiction.py <module-name> >>pydiction
# Example: The following will append all the time module's methods to the file "pydiction" with 
#          and without the "time." prefix:   pydiction.py time >>pydiction
import sys


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("%s requires one argument\n" % sys.argv[0])
        sys.exit()

    modname = sys.argv[1]

    try:
        exec "import " + modname
    except ImportError:
        sys.stdout.write("ImportError: No module named: %s\n" % modname)
        return
    except:
        return

    mod_contents = dir(eval(modname))

    # prefix module name
    print "\n-- %s module with \"%s.\" prefix --" % (modname, modname)
    for i in mod_contents:
        if callable(eval(modname + '.' + i)):
            # it's a function so append a '(' for the auto-completion
            print modname + '.' + i + '('
        else:
            print modname + '.' + i    

    # don't prefix module name
    print "\n-- %s module without \"%s.\" prefix --" % (modname, modname)
    for i in mod_contents:
        if callable(eval(modname + '.' + i)):
            print i + '('
        else:
            print i


if __name__ == '__main__':
    main()
