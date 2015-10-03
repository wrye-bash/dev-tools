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
ORG_NAME = u'Wrye Bash'
TOKEN = '31ed03d9b3975325adf40cf9fc5ffacc39fc99f8'

GAMES = {
    # Convert to display names
    'skyrim': u'Skyrim',
    'oblivion': u'Oblivion',
    'fallout': u'Fallout 3',
    'fnv': u'Fallout - New Vegas',
}

MAIN_LABELS = {'bug', 'enhancement'}
REJECTED_LABELS = {'duplicate', 'rejected', 'wont fix', 'works for me',
                   'backburner', 'invalid','regression', 'needinfo', }
DEV_LABELS = {'TODO', 'discussion', 'git', 'goal', 'question'}
PROGRESS_LABELS = {'review'}
TAGGING_LABELS = {'docs', 'svn', 'patcher', 'wx', 'bain', 'wine'}
GAME_LABELS = set(GAMES.keys()) | {'morrowind'}
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

# LOGIN =======================================================================
from helpers import github_wrapper

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

def hub(opts, deadMilestone=False):
    # Login
    git = _login(opts)
    if not git: return
    repo = _getRepo(git)
    if not repo: return
    milestone = _getMiles(opts, repo)
    if not milestone and not deadMilestone: return
    return repo, milestone

# OUTPUT & TEMPLATES DIRs =====================================================
import os, shutil

OUT_DIR = u'out'
TEMPLATES_DIR = u'templates'

def _cleanOutDir(path=OUT_DIR):
    # Clean output directory
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except:
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
