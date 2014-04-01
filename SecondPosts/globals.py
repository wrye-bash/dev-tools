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

"""This module exports global constants for the scripts that generate the
posts. Those constants are special to the wrye-bash/wrye-bash repository. If
the scripts are to be used for other repos too we need a repo factory here."""

REPO_NAME = u'wrye-bash'
ORG_NAME = u'Wrye Bash'
TOKEN = '31ed03d9b3975325adf40cf9fc5ffacc39fc99f8'

GAMES = {
    # Convert to display names
    'skyrim': u'Skyrim',
    'oblivion': u'Oblivion',
    'fallout': u'Fallout 3',
    'fnv': u'Fallout - New Vegas',
}

DEV_LABELS = {'git', 'goal', 'discussion', 'TODO', 'wont fix', 'works for me',
               'rejected', 'duplicate'}
GAME_LABELS = set(GAMES.keys())
SKIP_LABELS = DEV_LABELS

URL_MILESTONE = \
    'https://github.com/wrye-bash/wrye-bash/issues?milestone=%i&state=open'
URL_BUGS = 'https://github.com/wrye-bash/wrye-bash/issues?labels=bug'
URL_ENHANCEMENTS = \
    'https://github.com/wrye-bash/wrye-bash/issues?labels=enhancement'

# LOGIN ========================================
import github_wrapper

def _login(opts):
    """Login to github . Return None if failed to login"""
    if opts.user:
        user = github_wrapper.getUser()
    else:
        user = (TOKEN,)
    print "Logging in..."
    git = github_wrapper.getGithub(*user)
    if not git: return None
    try:
        print "User:", github_wrapper.getUserName(git)
    except github_wrapper.GithubApiException as e:
        print e.message
        return None
    return git

def _getRepo(github):
    print "Getting repository..."
    repo = github_wrapper.getRepo(github, ORG_NAME, REPO_NAME)
    if not repo:
        print 'Could not find repository:', REPO_NAME
    return repo

def _getMiles(opts, repo):
    print "Getting Milestone..."
    milestone = github_wrapper.getMilestone(repo, opts.milestone)
    if not milestone:
        print 'Could not find milestone:', opts.milestone
    return milestone

# OUTPUT DIR =====================================
import os, shutil

OUT_DIR = u'out'

def _cleanOutDir(path=OUT_DIR):
    # Clean output directory
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except:
            pass

def _outFile(dir_=OUT_DIR, name="out.txt"):
    if not os.path.exists(dir_):
        os.makedirs(dir_)
    outFile = os.path.join(dir_, name)
    return outFile

# Arguments Parser =====================================
import argparse

class Parser:
    def __init__(self, prog, add_help=True):
        self.parser = argparse.ArgumentParser(prog=prog, add_help=add_help)

    @staticmethod
    def new(prog, add_help=True):
        return Parser(prog, add_help)

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
        self.parser.add_argument('-m', '--milestone',
                                 dest='milestone',
                                 action='store',
                                 type=str,
                                 required=True,
                                 help=help_)
        return self

    def user(self):
        self.parser.add_argument('-u', '--user',
                                 dest='user',
                                 action='store_true',
                                 default=False,
                                 help='Force usage of a different user to '
                                      'pull info.')
        return self

    def parse(self):
        return self.parser.parse_args()
