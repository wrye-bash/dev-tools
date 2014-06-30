# -*- coding: utf-8 -*-
#
# GPL License and Copyright Notice ============================================
# This file is part of Wrye Bash.
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
from globals import SKIP_LABELS, Parser, _outFile, hub

# Functions ===================================================================
def _parseArgs():
    return Parser.new(prog='Generate Changelog').user().milestone(
        help_='Specify the milestone for latest release.').games(
        help_='Show closed issues for a specific game only.',
        helpAll='Show closed issues for all games.').parse()

from html import h2, ul, bbList, size, markdownList, \
    CHANGELOG_TITLE_SIZE  # TODO this has no place here

def _title(milestone, authors=('Various community members',)):
    # TODO - get authors from issues
    title = milestone.title + ' [' + date.today().strftime('%Y/%m/%d') + '] '
    if not authors: return title
    return title + '[' + ", ".join(authors) + ']'

# API =========================================================================
from html import closedIssue
import os.path

CHANGELOGS_DIR = '../ChangeLogs'

def writeChangelog(issues, milestone, overwrite=False):
    """Write 'Changelog - <milestone>.txt'"""
    outFile = _outFile(dir_=CHANGELOGS_DIR,
                       name=u'Changelog - ' + milestone.title + u'.txt')
    if os.path.isfile(outFile) and not overwrite: return outFile
    with open(outFile, 'w') as out:
        out.write(h2(_title(milestone)))
        out.write('\n'.join(ul(issues, closedIssue)))
        out.write('\n')
        # out.write('\n'.join(ul(issues, closedIssueLabels)))
        # out.write('\n')
    return outFile

def writeChangelogBBcode(issues, milestone, overwrite=False):
    # TODO merge with writeChangelog()
    """Write 'Changelog - <milestone>.bbcode.txt'"""
    outFile = _outFile(dir_=CHANGELOGS_DIR,
                       name=u'Changelog - ' + milestone.title + u'.bbcode.txt')
    if os.path.isfile(outFile) and not overwrite: return outFile
    with open(outFile, 'w') as out:
        out.write(size(CHANGELOG_TITLE_SIZE, _title(milestone)))
        out.write('\n' + '[spoiler]')
        out.write('\n'.join(bbList(issues, closedIssue)))
        out.write('\n' + '[/spoiler]')
        out.write('\n')
    return outFile

def writeChangelogMarkdown(issues, milestone, overwrite=False):
    # TODO merge with writeChangelog()
    """Write 'Changelog - <milestone>.markdown.txt'"""
    outFile = _outFile(dir_=CHANGELOGS_DIR,
                       name=u'Changelog - ' + milestone.title + u'.markdown')
    if os.path.isfile(outFile) and not overwrite: return outFile
    with open(outFile, 'w') as out:
        out.write( _title(milestone))
        out.write('\n\n')
        out.write('\n'.join(markdownList(issues, closedIssue)))
        out.write('\n')
    return outFile

def main():
    opts = _parseArgs()  # TODO per game # if opts.game:...
    # TODO add command line option to overwrite existing changelog
    git_ = hub(opts)
    if not git_: return
    repo, milestone = git_[0], git_[1]
    issues = getClosedIssues(repo, milestone, skip_labels=SKIP_LABELS)
    print 'Writing changelogs'
    writeChangelog(issues, milestone)
    writeChangelogMarkdown(issues, milestone)
    writeChangelogBBcode(issues, milestone)
    print 'Changelogs generated.'

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Aborted"
