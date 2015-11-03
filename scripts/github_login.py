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
from globals import TOKEN, ORG_NAME, REPO_NAME
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
        pass
        print "User:", github_wrapper.getUserName(git)
    except github_wrapper.GithubApiException as e:
        print e.message
        return None
    return git

def _getRepo(github):
    print "Getting repository..."
    repo = github_wrapper.getRepo(github, ORG_NAME, REPO_NAME)
    if not repo:
        print 'Could not find repository:', REPO_NAME, ' - aborting'
    return repo

def _getMiles(opts, repo):
    print "Getting Milestone..."
    milestone = github_wrapper.getMilestone(repo, opts.milestone)
    if not milestone:
        print 'Could not find milestone:', opts.milestone, ' - aborting'
    return milestone

def hub(opts, deadMilestone=False):
    # Login
    git = _login(opts)
    if not git:
        print 'Failed to login, aborting'
        return
    repo = _getRepo(git)
    if not repo: return
    milestone = None
    if not deadMilestone:
        milestone = _getMiles(opts, repo)
        if not milestone: return
    return repo, milestone

from cli_parser import Parser
from globals import ALL_LABELS
from helpers.github_wrapper import allLabels

if __name__ == '__main__':
    git_ = hub(Parser('no desc').user().parse(), deadMilestone=True)
    labels = set(x.name for x in allLabels(git_[0])) # github.Label.Label
    print labels
    print ALL_LABELS
    print labels == ALL_LABELS
