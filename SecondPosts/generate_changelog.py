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

"""This module generates the changelog reading metadata for a milestone."""
import argparse

from github_wrapper import *
from globals import TOKEN, GAMES, ORG_NAME, REPO_NAME

# Functions ===================================================================
def parseArgs():
    parser = argparse.ArgumentParser(prog='Generate Changelog',
                                     add_help=True)
    parser.add_argument('-m', '--milestone',
                        dest='milestone',
                        action='store',
                        type=str,
                        required=True,
                        help='Specify the milestone for latest release.')
    parser.add_argument('-u', '--user',
                        dest='user',
                        action='store_true',
                        default=False,
                        help='Force usage of a different user to pull info.')
    gameGroup = parser.add_mutually_exclusive_group()
    gameGroup.add_argument('-g', '--game',
                           dest='game',
                           type=str,
                           choices= ['skyrim',
                                     'oblivion',
                                     'fallout',
                                     'fnv',
                                     ],
                           help='Show issues for a specific game only.')
    gameGroup.add_argument('-a', '--all',
                           dest='all',
                           action='store_true',
                           default=False,
                           help='Show issues for all games.')
    return parser.parse_args()

def _login(opts):
    """login - . Returns false if failed to login""" # TODO globals.py
    if opts.user:
        user = getUser()
    else:
        user = (TOKEN,)
    print "Logging in..."
    git = getGithub(*user)
    if not git: return False # TODO: needed ?
    print "User:", git.get_user().name
    print "Getting repository..."
    repo = getRepo(git, ORG_NAME, REPO_NAME)
    if not repo:
        print 'Could not find repository:', REPO_NAME
        return False
    print "Getting Milestone..."
    milestone = getMilestone(repo, opts.milestone)
    if not milestone:
        print 'Could not find milestone:', opts.milestone
        return False
    return True

def _outDir(path = u'out'):
     # Clean output directory
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except:
            pass

def main():
    """Start everything off"""
    opts = parseArgs()
    # Figure out which games to do:
    if opts.game:
        games = {opts.game: GAMES[opts.game]}
    else:
        games = GAMES
    # Login
    if not _login(opts): return
    # Output directory
    _outDir()
    # Create posts
    for game in games:
        print 'Getting Issues for:', games[game]
        issues = getIssues(repo, milestone, game)
        print 'Writing changelog'
        writeChangelog(games[game], milestone, issues)
    print 'Second post(s) generated.'

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Aborted"
