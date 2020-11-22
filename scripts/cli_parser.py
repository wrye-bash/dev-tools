#!/usr/env/bin python2-32
# -*- coding: utf-8 -*-
#
# GPL License and Copyright Notice ============================================
#  This file is part of Wrye Bash.
#
#  Wrye Bash is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  Wrye Bash is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Wrye Bash; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#  Wrye Bash copyright (C) 2005-2009 Wrye, 2010-2015 Wrye Bash Team
#  https://github.com/wrye-bash
#
# =============================================================================

"""This module's Parse class is responsible for parsing the command line
arguments to the scripts. Default behavior of the scripts is defined in this
class"""
from __future__ import absolute_import, print_function

import argparse
import os

from globals import DEFAULT_MILESTONE_TITLE, DEFAULT_AUTHORS

PROMPT = u'PROMPT'

class Parser(object):
    def __init__(self, description, add_h=True):
        self.parser = argparse.ArgumentParser(description=description,
                        add_help=add_h,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        # actions to be run on options if not specified
        self.actions = []

    def milestone(self, help_=u'Specify the milestone for latest release.'):
        action = self.parser.add_argument(u'-m', u'--milestone',
            dest=u'milestone', default=PROMPT, type=unicode, help=help_)
        self.actions.append(action)
        return self

    def milestone_title(self,
            help_=u'Specify a title for the milestone changelog.'):
        action = self.parser.add_argument(u'-t', u'--title', dest=u'title',
            default=DEFAULT_MILESTONE_TITLE, type=unicode, help=help_)
        self.actions.append(action)
        return self

    def overwrite(self):
        self.parser.add_argument(u'-o', u'--overwrite', dest=u'overwrite',
            action=u'store_false', help=u'Do NOT overwrite existing file(s)')
        return self

    def offline(self):
        self.parser.add_argument(u'--offline', dest=u'offline',
            action=u'store_true', help=u'Do not hit github - you must have '
                                       u'the issue list available offline')
        return self

    def editor(self, help_=u'Path to editor executable to launch.',
               help_no_editor=u'Never launch an editor'):
        editor_group = self.parser.add_mutually_exclusive_group()
        editor_group.add_argument(u'-e', u'--editor', dest=u'editor',
            default=os.path.expandvars(os.path.join(
                u'%PROGRAMFILES%', u'Notepad++', u'notepad++.exe')),
            type=unicode, help=help_)
        editor_group.add_argument(u'-ne', u'--no-editor', dest=u'no_editor',
            action=u'store_true', default=False, help=help_no_editor)
        return self

    def authors(self, help_=u'Specify the authors (comma separated strings as '
                            u'in: Me,"Some Others".'):
        action = self.parser.add_argument(u'--authors', dest=u'authors',
            default=DEFAULT_AUTHORS, type=unicode, help=help_)
        self.actions.append(action)
        return self

    @staticmethod
    def get_editor(args):
        """Handles default fallbacks for the --editor option"""
        if not hasattr(args, u'editor'):
            if hasattr(args, u'no_editor'):
                args.editor = None
            return
        if os.path.exists(args.editor):
            return
        path = os.path.normcase(args.editor)
        path = os.path.normpath(path)
        path = os.path.expandvars(path)
        parts = path.split(os.path.sep)
        # If 'Program Files' was in the path, try 'Program Files (x86)',
        # and vice versa
        part1 = os.path.normcase(u'Program Files')
        part2 = os.path.normcase(u'Program Files (x86)')
        check = u''
        if part1 in parts:
            idex = parts.index(part1)
            parts[idex] = part2
            check = os.path.join(*parts)
        elif part2 in parts:
            idex = parts.index(part2)
            parts[idex] = part1
            check = os.path.join(*parts)
        if check and os.path.exists(check):
            args.editor = check
            return
        print(u'Specified editor does not exist, please enter a valid path:')
        check = raw_input('>')
        if not check:
            args.no_editor = True
        if not os.path.exists(check):
            print(u'Specified editor does not exists, assuming --no-editor')
            args.no_editor = True
        else:
            args.editor = check
        if args.no_editor:
            args.editor = None

    def parse(self):
        """
        Return an object which can be used to get the arguments as in:
            parser_instance.parse().milestone

        :return: ArgumentParser
        """
        args = self.parser.parse_args()
        # see: http://stackoverflow.com/a/21588198/281545
        for a in self.actions:
            if getattr(args, a.dest) == a.default and a.default == PROMPT:
                print(u'Please specify %s' % a.dest)
                values = raw_input('>')
                setattr(args, a.dest, values)
        # Special handler for --editor:
        Parser.get_editor(args)
        return args
