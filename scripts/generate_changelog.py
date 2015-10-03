#!/usr/bin/env python2
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

"""This module generates the changelog for a milestone reading its metadata."""
from datetime import date
from cli_parser import Parser

CHANGELOG_TITLE_SIZE = 5

# Functions ===================================================================
def _parseArgs():
    return Parser(description='Generate Changelog').user().milestone(
        help_='Specify the milestone for latest release.').games(
        help_='Show closed issues for a specific game only.',
        helpAll='Show closed issues for all games.').overwrite(
    ).milestoneTitle().parse()

from helpers.html import h2, ul, bbList, size, markdownList, spoiler

def _title(title, authors=('Various community members',)):
    # TODO - get the authors from issues instead of passing them in
    title = title + '[' + date.today().strftime('%Y/%m/%d') + ']'
    if not authors: return title
    return title + ' [' + ", ".join(authors) + ']'

from helpers.html import closedIssue

def _changelog_bbcode(issues, title, outFile):
    with open(outFile, 'w') as out:
        out.write(size(CHANGELOG_TITLE_SIZE, _title(title)))
        out.write('\n'.join(spoiler('\n'.join(bbList(issues, closedIssue)))))
        out.write('\n')
    return outFile

def _changelog_txt(issues, title, outFile):
    with open(outFile, 'w') as out:
        out.write(h2(_title(title)))
        out.write('\n'.join(ul(issues, closedIssue)))
        out.write('\n\n')  # needs blank line for Version History.html
    return outFile

def _changelog_markdown(issues, title, outFile):
    with open(outFile, 'w') as out:
        out.write(_title(title))
        out.write('\n\n')
        out.write('\n'.join(markdownList(issues, closedIssue)))
        out.write('\n')
    return outFile

def _changelog_master(issues, dev_issues, title, outFile):
    with open(outFile, 'w') as out:
        out.write(_title(title, authors=None))
        out.write('\n\n')
        out.write('\n'.join(markdownList(issues, closedIssue)))
        out.write('\n\n')
        out.write('Internal issues fixed')
        out.write('\n\n')
        out.write('\n'.join(markdownList(dev_issues, closedIssue)))
        out.write('\n')
    return outFile

# API =========================================================================
import os.path
from globals import SKIP_LABELS, outPath, hub, DEFAULT_MILESTONE_TITLE, \
    REJECTED_LABELS, DEV_LABELS
from helpers.github_wrapper import getClosedIssues

CHANGELOGS_DIR = '../ChangeLogs'
def writeChangelog(repo, milestone, title=DEFAULT_MILESTONE_TITLE,
                   overwrite=False, extension=u'.txt', logic=_changelog_txt,
                   milestoneNumber=str(305)):
    """Write 'Changelog - <milestone>.txt'"""
    num = milestone.title if milestone else milestoneNumber
    outFile = outPath(dir_=CHANGELOGS_DIR,
                      name=u'Changelog - ' + num + extension)
    if os.path.isfile(outFile) and not overwrite: return outFile
    title = num + " " + title + " " if title else num
    issues = getClosedIssues(repo,milestone,skip_labels=SKIP_LABELS)
    return logic(issues,title,outFile)

def writeChangelogMaster(repo, milestone, title=DEFAULT_MILESTONE_TITLE,
                         overwrite=False, extension=u'.txt',
                         logic=_changelog_master):
    """Write 'Changelog - <milestone>.txt'"""
    if title: title = milestone.title + " " + title + " "
    else: title = milestone.title
    outFile = outPath(dir_=CHANGELOGS_DIR,
                      name=u'Master Commit Changelog - ' + milestone.title +
                           extension)
    if os.path.isfile(outFile) and not overwrite: return outFile
    issues = getClosedIssues(repo, milestone, skip_labels=SKIP_LABELS)
    dev_issues = getClosedIssues(repo, milestone, skip_labels=REJECTED_LABELS,
                                 keep_labels=DEV_LABELS)
    return logic(issues, dev_issues, title, outFile)

def writeChangelogBBcode(repo, milestone, title=None, overwrite=False,
                         num=str(305)):
    """Write 'Changelog - <milestone>.bbcode.txt'"""
    return writeChangelog(repo, milestone, title, overwrite,
                          extension=u'.bbcode.txt', logic=_changelog_bbcode,
                          milestoneNumber=num)

def writeChangelogMarkdown(repo, milestone, title=None, overwrite=False):
    """Write 'Changelog - <milestone>.markdown.txt'"""
    return writeChangelog(repo, milestone, title, overwrite,
                          extension=u'.markdown', logic=_changelog_markdown)

def main():
    opts = _parseArgs()  # TODO per game # if opts.game:...
    git_ = hub(opts)
    if not git_: return
    repo, milestone = git_[0], git_[1]
    print 'Writing changelogs'
    writeChangelog(repo, milestone, opts.title, opts.overwrite)
    writeChangelogMarkdown(repo, milestone, opts.title, opts.overwrite)
    writeChangelogBBcode(repo, milestone, opts.title, opts.overwrite)
    writeChangelogMaster(repo, milestone, opts.title, opts.overwrite)
    print 'Changelogs generated.'

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Aborted"
