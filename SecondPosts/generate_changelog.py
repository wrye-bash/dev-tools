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

"""This module generates the changelog for a milestone reading its metadata."""
from datetime import date
from github_wrapper import getClosedIssues
from globals import SKIP_LABELS, Parser, _login, _getRepo, _outFile, _getMiles

# Functions ===================================================================
def _parseArgs():
    return Parser.new(prog='Generate Changelog').user().milestone(
        help_='Specify the milestone for latest release.').games(
        help_='Show issues for a specific game only.',
        helpAll='Show issues for all games.').parse()

# TEMPLATE = u'changelog_template.txt'
from html import h2, ul

def _title(milestone, authors=('Various community members',)):
    # TODO - get authors from issues
    return h2(milestone.title + ' [' + date.today().strftime(
        '%Y/%m/%d') + '] ' + '[' + ", ".join(authors) + ']'
    )

# API =========================================================================
from html import closedIssue

def writeChangelog(milestone, issues):
    """Write 'Changelog - <milestone>.txt'"""
    outFile = _outFile(name=u'Changelog - ' + milestone.title + u'.txt')
    with open(outFile, 'w') as out:
        # with open(TEMPLATE,'r') as ins:
        out.write(_title(milestone))
        out.write('\n'.join(ul(issues, closedIssue)))
        out.write('\n\n')
        # out.write('\n'.join(ul(issues, closedIssueLabels)))
        # out.write('\n')

def main():
    opts = _parseArgs()  # TODO per game # if opts.game:...
    # Login # TODO move this to globals !!! same code in all main()s
    git = _login(opts)
    if not git: return
    repo = _getRepo(git)
    if not repo: return
    milestone = _getMiles(opts, repo)
    if not milestone: return
    issues = getClosedIssues(repo, milestone, skip_labels=SKIP_LABELS)
    print 'Writing changelog'
    writeChangelog(milestone, issues)
    print 'Changelog generated.'

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Aborted"
