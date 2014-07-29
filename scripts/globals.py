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

MAIN_LABELS = {'bug', 'docs', 'enhancement'}
REJECTED_LABELS = {'duplicate', 'rejected', 'wont fix', 'works for me'}
DEV_LABELS = {'TODO', 'discussion', 'git', 'goal', 'question', 'wxPyGUI'}
PROGRESS_LABELS = {'in progress', 'ready', 'svn'}
GAME_LABELS = set(GAMES.keys()) | {'morrowind'}
SKIP_LABELS = DEV_LABELS | REJECTED_LABELS
ALL_LABELS = MAIN_LABELS | REJECTED_LABELS | DEV_LABELS | PROGRESS_LABELS | \
             GAME_LABELS

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

# LOGIN ========================================
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

def hub(opts):
    # Login
    git = _login(opts)
    if not git: return
    repo = _getRepo(git)
    if not repo: return
    milestone = _getMiles(opts, repo)
    if not milestone: return # FIXME when I close a milestone this is None
    # so generate first posts won't run - grrr
    return repo, milestone

# OUTPUT DIR =====================================
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

def outPath(dir_=OUT_DIR, subdir='', name="out.txt"):
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

# Arguments Parser =====================================
import argparse

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
