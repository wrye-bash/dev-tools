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
from scripts.helpers.html import size, color

LATEST_BASH = '306'

class _Game(object):
    def __init__(self, display, patch=None, nexusUrl=None, prev_thread=None,
                 cur_thread=None, game_nexus_notes='',
                 minimum_bash_version=LATEST_BASH):
        self.display = display
        self.patch = patch
        self.nexusUrl = nexusUrl
        self.prev_thread = prev_thread
        self.cur_thread = cur_thread
        self.game_nexus_notes = game_nexus_notes
        self.minimum_bash_version = minimum_bash_version

OBLIVION = _Game(u'Oblivion', '1.2.0416',
    u'[url=http://www.nexusmods.com/oblivion/mods/22368]Oblivion Nexus[/url]',
                 _ini_parser.previous_oblivion_thread(),
                 _ini_parser.current_oblivion_thread())

SKYRIM = _Game(u'Skyrim', '1.9.32.0.8',
    u'[url=http://www.nexusmods.com/skyrim/mods/1840]Skyrim Nexus[/url]',
               game_nexus_notes=
    size(3, color('#3366ff', """Can Wrye Bash merge Mods?""")) + '\n\n' +
    color('red', ' '. join([line.strip() for line in
"""Note: Wrye Bash can not merge mods that add new records to Skyrim. It can
only merge mods that overwrite a previous master. If a mod alters
Skyrim.esm, or any other ESM from the Nexus, it can be merged into the Bash
Patch. As an example a mod like Immersive Armors introduces new records to
Skyrim and can not be merged.  However, just like Immersive Armors the vast
majority of Skyrim mods add new records. This means there is no way to load
300, 400, or 500 mods and still be under the safe limit of 254 mods max.
That number is 0 to 254 or, 255 mods. Skyrim.esm is always (00), Update.esm
is always, (01) and so on.""".splitlines()])))

FALLOUT4 = _Game(u'Fallout 4', '1.8.7.0',
    u'[url=http://www.nexusmods.com/fallout4/mods/20032]Fallout 4 Nexus[/url]',
                 minimum_bash_version='307.beta1')

SKYRIMSE = _Game(u'Skyrim Special Edition', '1.2.39.0.8',
    u'[url=http://www.nexusmods.com/skyrimspecialedition/mods/6837]'
    u'Skyrim Special Edition Nexus[/url]',
                 minimum_bash_version='307.beta1')


GAMES = OrderedDict([
    ('oblivion', OBLIVION), ('skyrim', SKYRIM), ('fallout4', FALLOUT4),
    ('skyrim-se', SKYRIMSE), ])

ALL_GAMES = OrderedDict([('oblivion', OBLIVION), ('skyrim', SKYRIM),
                         ('fallout4', FALLOUT4),
                         ('fallout3', _Game(u'Fallout 3')),
                         ('fnv', _Game(u'Fallout - New Vegas')),
                         ('skyrim-se', SKYRIMSE),
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
