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

"""Generates the second posts (bug list, etc) for all applicable sub-forums of
   Bethesda's forums.

   Usage:
     generate_second_posts.py -m MILESTONE {-g GAME | -a}

   For a complete list of -g arguments, you can also run:
     generate_second_posts.py -h

   MILESTONE is required, either a -g GAME for a specific game or -a/-all
   to generate all seconds posts is required.

   Requires PyGithub installed: https://github.com/jacquev6/PyGithub

   Generated seconds posts will be output to ./out
   """

# Imports ====================================================================
import os
import re
# Internal
from helpers.github_wrapper import *
from helpers.html import color, url, bbList, spoiler, strike, closedIssue

# Globals ====================================================================
from globals import outPath, URL_MILESTONE, URL_BUGS, URL_ENHANCEMENTS, \
    SKIP_LABELS, templatePath, ALL_GAMES
import github_login
from cli_parser import Parser

TEMPLATE = templatePath(name=u'generate_second_posts_lines.txt')

COLOR_INTRO = 'orange'
COLOR_ASSIGNEE = '#00FF00'
COLOR_DONE = 'orange'

# Functions ===================================================================
def parseArgs():
    return Parser(description='Generate Second Posts').milestone(
        help_='Specify the milestone for filtering Issues.').parse()

def getSecondPostLine(ins):
    """Reads lines from ins until a blank line is found, then joins the lines
       together (without newlines).   It's done this way so the source file is
       more readable when editing.
       ins: file-like object in read mode
       return: the reconstructed text"""
    lines = []
    for line in ins:
        line = line.strip('\r\n')
        if line:
            lines.append(line)
        else:
            break
    return ''.join(lines)

def _listOrNone(issues, issue_type):
    if issues:
        return '\n'.join(bbList(issues, formatIssue, issue_type))
    else:
        return '\n'.join(bbList([None]))

def writeSecondPost(gameTitle, milestone, issues):
    """Write 'Buglist thread Starter - <gameTitle>.txt'"""
    out_path = outPath(name=u'Buglist thread Starter - ' + gameTitle + u'.txt',
                      subdir='SecondPosts')
    with open(out_path, 'w') as out:
        print u'File:', os.path.abspath(out_path)
        with open(TEMPLATE, 'r') as ins: # TODO: real template
            # Intro paragraph
            line = getSecondPostLine(ins)
            out.write(color(COLOR_INTRO, line % milestone.title))
            out.write(getSecondPostLine(ins))
            out.write('\n\n')
            # Upcoming release
            line = getSecondPostLine(ins)
            out.write(url(URL_MILESTONE % milestone.title,
                          line % milestone.title))
            out.write('\n')
            # Write those damn issues
            out.write(_listOrNone(issues[0], 'Bug'))
            out.write(_listOrNone(issues[1], 'Enhancement'))
            # Other known bugs
            out.write(url(URL_BUGS, getSecondPostLine(ins)))
            out.write('\n'.join(spoiler(_listOrNone(issues[2], 'Bug'))))
            # Other known feature requests
            out.write((url(URL_ENHANCEMENTS, getSecondPostLine(ins))))
            out.write('\n'.join(spoiler(_listOrNone(issues[3], 'Enhancement'))))
            out.write('\n\n')
            line = getSecondPostLine(ins)
            out.write(line + '\n\n')
            line = getSecondPostLine(ins)
            out.write(line + '\n\n')
            line = getSecondPostLine(ins)
            out.write(line + '\n')

def _getIssuesForPosts(repo, milestone):
    """Return a tuple of applicable issues for the given game and milestone
        repo: github.Repository object
        milestone: github.Milestone object
        gameLabel: label for the specific game (ie: `skyrim`, `fnv`, etc). Only
          issues for this game will be returned
       return:
        (current_bug, current_enh, other_bug, other_enh)
        where:
          current_bug: Issues tagged `bug` for milestone
          current_enh: Issues tagged `enhancement` for milestone
          other_bug: Issues tagged `bug`, but not for this milestone
          other_enh: Issues tagged `enhancement`, but not for this milestone
    """
    skip_labels = SKIP_LABELS
    getIssues(repo) # get all issues to fill the cache # FIXME delete this ?
    current_bug = getIssues(repo, milestone, keep_labels={'bug'},
                            skip_labels=skip_labels)
    current_enh = getIssues(repo, milestone, keep_labels={'enhancement'},
                            skip_labels=skip_labels)
    other_bug = getIssues(repo, keep_labels={'bug'},
                          skip_labels=skip_labels, state='open')
    other_enh = getIssues(repo, keep_labels={'enhancement'},
                          skip_labels=skip_labels, state='open')
    # exclude current milestones issues from other_
    milestone_title = milestone.title
    other_bug = [x for x in other_bug if
                 not x.milestone or x.milestone.title != milestone_title]
    other_enh = [x for x in other_enh if
                 not x.milestone or x.milestone.title != milestone_title]
    # Sort current_bug/enh: already sorted by date, just move the
    # open issues to the top
    current_bug = [x for x in current_bug if x.state in ('open', 'closed')]
    current_enh = [x for x in current_enh if x.state in ('open', 'closed')]
    return current_bug, current_enh, other_bug, other_enh

# Display =====================================
def closedIssueLabels(issue):
    """String representation (see closedIssue()) plus labels"""
    return closedIssue(issue) + ' - ' + str(
        set(x.name for x in issue.get_labels()))

def formatIssue(issue, issueType):
    """Formats the issue striking it through if closed.

    :rtype : str
    """
    if issue.state == 'open':
        s = lambda x: x
    else:
        s = lambda x: color(COLOR_DONE, strike(x))
    if issue.assignee:
        assignee = issue.assignee
        assignee = ' ' + url(assignee.url,
                             color(COLOR_ASSIGNEE, '(' + assignee.login + ')'))
    else:
        assignee = ''
    game_labels= set(ALL_GAMES) & set(issue.labels)
    games = []
    for game in game_labels:
        if not re.search(game, issue.title, re.I):
            games.append(ALL_GAMES[game].display)
    games = ', '.join(games)
    return s(url(issue.html_url,issueType + ' %i' % issue.number) + ': ' + (
    '[' + games + '] ' if games else '') + issue.title) + assignee

def main():
    """Start everything off"""
    opts = parseArgs()
    git_ = github_login.hub(opts.milestone)
    if not git_: return
    repo, milestone = git_[0], git_[1]
    issues = _getIssuesForPosts(repo, milestone)
    print 'Writing second post...'
    writeSecondPost(u'Oblivion', milestone, issues)
    print 'Second post generated.'

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Aborted"
