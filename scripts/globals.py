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

"""This module exports global constants for the scripts that generate the
posts. Those constants are special to the wrye-bash/wrye-bash repository. If
the scripts are to be used for other repos too we need a repo factory here."""

REPO_NAME = u'wrye-bash'
ORG_NAME = u'wrye-bash'

# GAMES =======================================================================
from helpers import ini_parser as _ini_parser
from collections import OrderedDict

class _Game(object):
    def __init__(self, display, nexusUrl=None, prev_thread=None,
                 cur_thread=None):
        self.display = display
        self.nexusUrl = nexusUrl
        self.prev_thread = prev_thread
        self.cur_thread = cur_thread

OBLIVION = _Game(u'Oblivion', u'[url=http://www.nexusmods.com/'
                              u'oblivion/mods/22368]Oblivion Nexus[/url]',
                 _ini_parser.previous_oblivion_thread(),
                 _ini_parser.current_oblivion_thread())
SKYRIM = _Game(u'Skyrim', u'[url=http://www.nexusmods.com/'
                          u'skyrim/mods/1840]Skyrim Nexus[/url]',
               _ini_parser.previous_skyrim_thread(),
               _ini_parser.current_skyrim_thread())
FALLOUT4 = _Game(u'Fallout 4', u'[url=http://www.nexusmods.com/'
                               u'fallout4/mods/3699]Fallout 4 Nexus[/url]')

GAMES = OrderedDict(
    [('oblivion', OBLIVION), ('skyrim', SKYRIM), ('fallout4', FALLOUT4), ])

ALL_GAMES = OrderedDict([('oblivion', OBLIVION), ('skyrim', SKYRIM),
                         ('fallout4', FALLOUT4),
                         ('fallout3', _Game(u'Fallout 3')),
                         ('fnv', _Game(u'Fallout - New Vegas')),
                         ('skyrim-se', _Game(u'Skyrim Special Edition')),
                         ])

MAIN_LABELS = {'bug', 'enhancement'}
REJECTED_LABELS = {'duplicate', 'rejected', 'wont fix', 'works for me',
                   'backburner', 'invalid','regression', }
DEV_LABELS = {'TODO', 'discussion', 'git', 'goal', 'question'}
PROGRESS_LABELS = {'review'}
TAGGING_LABELS = {'docs', 'svn', 'patcher', 'wx', 'bain', 'wine', 'needinfo'}
GAME_LABELS = set(ALL_GAMES.keys()) | {'morrowind'}
# unions
SKIP_LABELS = DEV_LABELS | REJECTED_LABELS
ALL_LABELS = MAIN_LABELS | REJECTED_LABELS | DEV_LABELS | PROGRESS_LABELS | \
             GAME_LABELS | TAGGING_LABELS

URL_ISSUES = 'https://github.com/wrye-bash/wrye-bash/issues'
# URL_MILESTONE is used in string formatting, '%' needs to be
# escaped as '%%'
URL_MILESTONE = (
    URL_ISSUES + '?q=milestone%%3A%s+is%%3Aissue+is%%3Aopen'
    )
URL_BUGS = (
    URL_ISSUES + '?q=is%3Aissue+is%3Aopen+label%3Abug'
    )
URL_ENHANCEMENTS = (
    URL_ISSUES + '?q=is%3Aissue+is%3Aopen+label%3Aenhancement'
    )

DEFAULT_MILESTONE_TITLE = 'Bug fixes and enhancements'
DEFAULT_AUTHORS = 'Various community members'

# OUTPUT & TEMPLATES DIRs =====================================================
import os, shutil

OUT_DIR = u'out'
TEMPLATES_DIR = u'templates'

def _cleanOutDir(path=OUT_DIR):
    # Clean output directory
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except OSError:
            pass

def outPath(dir_=OUT_DIR, subdir=u'', name=u"out.txt"):
    """Returns a path joining the dir_ and name parameters. Will create the
    dirs in dir_ if not existing.

    :param dir_: a directory path
    :param name: a filename
    """
    dir_ = os.path.join(dir_, subdir)
    if not os.path.exists(dir_):
        os.makedirs(dir_)
    return os.path.join(dir_, name)

def templatePath(dir_=TEMPLATES_DIR, name=''):
    """Returns a template path to use when building a page/post.

    :param dir_: the directory the templates are in.
    :param name: the filename of a specific template file.
    :return: :raise IOError: when the file does not exist
    """
    outFile = os.path.join(dir_, name)
    if not os.path.exists(outFile):
        raise IOError('Template file must exist')
    return outFile
