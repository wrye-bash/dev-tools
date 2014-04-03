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
#  Wrye Bash copyright (C) 2005-2009 Wrye, 2010-2014 Wrye Bash Team
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

   The script uses the 'wrye-bash-automoton' user on GitHub, which is a
   read-only member of the wrye-bash repository.  A Personal Access Token
   has been generated and is hard coded in this tool.

   If you need or want to use your own user to pull the information, you
   must pass '-u' on the command line, which will read
   'generate_second_posts.usr' for your user/password or access token.AMPER
   It is *highly recommended* to use an access token (requires 2-factor
   authentication) so your password isn't stored in plain-text on your
   computer.  See the wiki on wrye-bash/meta on how to set this up.

   Generated seconds posts will be output to ./out
   """

# Imports ====================================================================
from github_wrapper import *
from html import color, COLOR_INTRO, url, formatIssue

# Globals ====================================================================
from globals import _outFile, Parser, URL_MILESTONE, URL_BUGS, \
    URL_ENHANCEMENTS, GAME_LABELS, SKIP_LABELS, GAMES, _template, hub

TEMPLATE = _template(name=u'generate_second_posts_lines.txt')

# Functions ===================================================================
def parseArgs():
    return Parser.new(prog='Generate Second Posts').user().games(
        help_='Generate a second post for a specific game.',
        helpAll='Generate a second post for all games.').milestone(
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

def writeSecondPost(gameTitle, milestone, issues):
    """Write 'Buglist thread Starter - <gameTitle>.txt'"""
    outFile = _outFile(name=u'Buglist thread Starter - ' + gameTitle + u'.txt')
    with open(outFile, 'w') as out:
        with open(TEMPLATE, 'r') as ins:
            # Intro paragraph
            line = getSecondPostLine(ins)
            out.write(color(line % milestone.title, COLOR_INTRO))
            out.write(getSecondPostLine(ins))
            out.write('\n\n')
            # Upcoming release
            line = getSecondPostLine(ins)
            out.write(url(URL_MILESTONE % milestone.id,
                          line % milestone.title))
            out.write('\n[list]\n')
            for issueList,issueType in ((issues[0],'Bug'),
                                        (issues[1],'Enhancement')):
                for issue in issueList:
                    out.write(formatIssue(issue, issueType))
                    out.write('\n')
            out.write('[/list]\n\n')
            # Other known bugs
            out.write(url(URL_BUGS, getSecondPostLine(ins)))
            out.write('\n[spoiler][list]\n')
            for issue in issues[2]:
                out.write(formatIssue(issue, 'Bug'))
                out.write('\n')
            if not issues[2]:
                out.write('None\n')
            out.write('[/list][/spoiler]\n\n')
            # Other known feature requests
            out.write((url(URL_ENHANCEMENTS, getSecondPostLine(ins))))
            out.write('\n[spoiler][list]\n')
            for issue in issues[3]:
                out.write(formatIssue(issue, 'Enhancement'))
                out.write('\n')
            if not issues[3]:
                out.write('None')
            out.write('[/list][/spoiler]\n')

def getIssuesForPosts(repo, milestone, gameLabel):
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
    skip_labels = GAME_LABELS - {gameLabel}  # what if gameLabel is None
    skip_labels = skip_labels | SKIP_LABELS
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
    #  open issues to the top
    current_bug = [x for x in current_bug if x.state in ('open', 'closed')]
    current_enh = [x for x in current_enh if x.state in ('open', 'closed')]
    return current_bug, current_enh, other_bug, other_enh

def main():
    """Start everything off"""
    opts = parseArgs()
    # Figure out which games to do:
    if opts.game:
        games = {opts.game: GAMES[opts.game]}
    else:
        games = GAMES
    git_ = hub(opts)
    if not git_: return
    repo, milestone = git_[0], git_[1]
    # print getUnlabeledIssues(repo)
    # all_ = getIssues(repo)
    # print [x.title for x in all_].__len__()
    # return
    # # Clean Output directory
    # _cleanOutDir()
    # Create posts
    # games = {'fnv': u'Fallout - New Vegas'}
    for game in games:
        print 'Getting Issues for:', games[game]
        issues = getIssuesForPosts(repo, milestone, game)
        print 'Writing second post...'
        writeSecondPost(games[game], milestone, issues)
    print 'Second post(s) generated.'

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Aborted"
