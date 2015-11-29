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
import argparse
import os
from globals import DEFAULT_MILESTONE_TITLE, DEFAULT_AUTHORS, ALL_GAMES, TOKEN
from scripts.helpers import github_wrapper

PROMPT = 'PROMPT'

class Parser:

    def __init__(self, description, add_h=True):
        self.parser = argparse.ArgumentParser(description=description,
                        add_help=add_h,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        # actions to be run on options if not specified
        self.actions = []

    def games(self, help_='Show issues for a specific game only.',
              helpAll='Show issues for all games.'):
        gameGroup = self.parser.add_mutually_exclusive_group()
        gameGroup.add_argument('-g', '--game',
                               dest='game',
                               type=str,
                               choices=ALL_GAMES.keys(),
                               help=help_)
        gameGroup.add_argument('-a', '--all',
                               dest='all',
                               action='store_true',
                               default=False,
                               help=helpAll)
        return self

    def milestone(self, help_='Specify the milestone for latest release.'):
        action = self.parser.add_argument('-m', '--milestone',
                                          dest='milestone',
                                          default=PROMPT,
                                          type=str,
                                          help=help_)
        self.actions.append(action)
        return self

    def milestoneTitle(self,
                       help_='Specify a title for the milestone changelog.'):
        action = self.parser.add_argument('-t', '--title',
                                          dest='title',
                                          default=DEFAULT_MILESTONE_TITLE,
                                          type=str,
                                          help=help_)
        self.actions.append(action)
        return self

    def user(self):
        self.parser.add_argument('-u', '--user',
                                 dest='user',
                                 action='store_true',
                                 default=False,
                                 help='Force usage of a different user to '
                                      'pull info.')
        return self

    def overwrite(self):
        self.parser.add_argument('-o', '--overwrite',
                                 dest='overwrite',
                                 action='store_false',
                                 help='Do NOT overwrite existing file(s)')
        return self

    def offline(self):
        self.parser.add_argument('--offline',
                                 dest='offline',
                                 action='store_true',
                                 help='Do not hit github - you must have the '
                                      'issue list available offline')
        return self

    def editor(self, help_='Path to editor executable to launch.',
               helpNoEditor='Never launch an editor'):
        editorGroup = self.parser.add_mutually_exclusive_group()
        editorGroup.add_argument('-e', '--editor',
                                 dest='editor',
                                 default=os.path.expandvars(
                                     os.path.join(
                                         u'%PROGRAMFILES%', u'Notepad++',
                                         u'notepad++.exe')),
                                 type=str,
                                 help=help_)
        editorGroup.add_argument('-ne', '--no-editor',
                                 dest='no_editor',
                                 action='store_true',
                                 default=False,
                                 help=helpNoEditor)
        return self

    def authors(self, help_='Specify the authors (comma separated strings as '
                            'in: Me,"Some Others".'):
        action = self.parser.add_argument('--authors',
                                          dest='authors',
                                          default=DEFAULT_AUTHORS,
                                          type=str,
                                          help=help_)
        self.actions.append(action)
        return self

    @staticmethod
    def getEditor(args):
        """Handles default fallbacks for the --editor option"""
        if not hasattr(args, 'editor'):
            if  hasattr(args, 'no_editor'):
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
        print 'Specified editor does not exist, please enter a valid path:'
        check = raw_input('>')
        if not check:
            args.no_editor = True
        if not os.path.exists(check):
            print 'Specified editor does not exists, assuming --no-editor'
            args.no_editor = True
        if args.no_editor: args.editor = None

    @staticmethod
    def getUser(args):
        if hasattr(args, 'user') :
            if args.user:
                user = github_wrapper.getUser()
            else:
                user = (TOKEN,)
            args.user = user

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
                print 'Please specify', a.dest
                values = raw_input('>')
                setattr(args, a.dest, values)
        # Special handler for --editor:
        Parser.getEditor(args)
        Parser.getUser(args)
        return args
