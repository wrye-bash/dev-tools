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
from globals import ORG_NAME, REPO_NAME
from helpers import github_wrapper

def _getRepo():
    print "Getting repository..."
    repo = github_wrapper.get_repo(ORG_NAME, REPO_NAME)
    if not repo:
        print 'Could not find repository:', REPO_NAME, ' - aborting'
    return repo

def _getMiles(milestoneNum, repo):
    print "Getting Milestone..."
    milestone = github_wrapper.get_milestone(repo, milestoneNum)
    if not milestone:
        print 'Could not find milestone:', milestoneNum, ' - aborting'
    return milestone

def hub(milestoneNum=None):
    repo = _getRepo()
    if not repo: return
    milestone = None
    if milestoneNum:
        milestone = _getMiles(milestoneNum, repo)
        if not milestone: return
    return repo, milestone
