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
from __future__ import absolute_import, print_function

from globals import ORG_NAME, REPO_NAME
from helpers import github_wrapper

def _get_repo():
    print(u'Getting repository...')
    repo = github_wrapper.get_repo(ORG_NAME, REPO_NAME)
    if not repo:
        print(u'Could not find repository: %s - aborting' % REPO_NAME)
    return repo

def _get_miles(milestone_num, repo):
    print(u'Getting Milestone...')
    milestone = github_wrapper.get_milestone(repo, milestone_num)
    if not milestone:
        print(u'Could not find milestone: %s - aborting' % milestone_num)
    return milestone

def hub(milestone_num=None):
    repo = _get_repo()
    if not repo: return
    milestone = None
    if milestone_num:
        milestone = _get_miles(milestone_num, repo)
        if not milestone: return
    return repo, milestone
