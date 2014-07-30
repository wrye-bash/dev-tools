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
#  Wrye Bash copyright (C) 2005-2009 Wrye, 2010-2014 Wrye Bash Team
#  https://github.com/wrye-bash
#
# =============================================================================

"""This module's Parse class is responsible for parsing teh command line
arguments to the scripts. Default behavior of the scripts is defined in this
class"""
import argparse
from globals import GAMES, DEFAULT_MILESTONE_TITLE

PROMPT = 'PROMPT'

class Parser:

    def __init__(self, desc, add_h=True):
        self.parser = argparse.ArgumentParser(description=desc, add_help=add_h,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        # actions to be run on options if not specified
        self.actions = []

    @staticmethod
    def new(description, add_help=True):
        return Parser(description, add_help)

    def games(self, help_='Show issues for a specific game only.',
              helpAll='Show issues for all games.'):
        gameGroup = self.parser.add_mutually_exclusive_group()
        gameGroup.add_argument('-g', '--game',
                               dest='game',
                               type=str,
                               choices=GAMES.keys(),
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

    def editor(self, help_='Path to editor executable to launch.',
               helpNoEditor='Never launch an editor'):
        editorGroup = self.parser.add_mutually_exclusive_group()
        editorGroup.add_argument('-e', '--editor',
                                 dest='editor',
                                 default='C:\\Program '
                                         'Files\\Notepad++\\notepad++.exe',
                                 type=str,
                                 help=help_)
        editorGroup.add_argument('-ne', '--no-editor',
                                 dest='no_editor',
                                 action='store_true',
                                 default=False,
                                 help=helpNoEditor)
        return self

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
        return args
