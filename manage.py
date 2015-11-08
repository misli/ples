#!/usr/bin/env python

from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

import os
import sys
from os.path import dirname, realpath, join

if __name__ == "__main__":
    sys.path.insert(0, join(dirname(realpath(__file__)), "app"))
    os.environ.setdefault("DEBUG", "TEMPLATE")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ples.settings")

    if os.getuid() == 0 and 'collectstatic' not in sys.argv:
        import pwd, grp
        user = pwd.getpwnam('django-ples')
        groups = [g.gr_gid for g in grp.getgrall() if user.pw_name in g.gr_mem]
        os.setgid(user.pw_gid)
        os.setgroups(groups)
        os.setuid(user.pw_uid)
        os.environ['USER']      = user.pw_name
        os.environ['LOGNAME']   = user.pw_name
        os.environ['HOME']      = user.pw_dir
        os.environ['SHELL']     = user.pw_shell
        try:
            os.chdir(os.environ['HOME'])
        except:
            pass

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
