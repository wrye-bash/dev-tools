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
#  Wrye Bash copyright (C) 2005-2009 Wrye, 2010-2014 wrye-bash
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
   must past '-u' on the command line, which will read
   'generate_second_posts.usr' for your user/password or access token.AMPER
   It is *highly recommended* to use an access token (requires 2-factor
   authentication) so you password isn't stored in plain-text on your
   computer.  See the wiki on wrye-bash/meta on how to set this up.

   Generated seconds posts will be output to ./out
   """


# Imports ====================================================================
import argparse
import shutil
from github_wrapper import *

# Globals ====================================================================
TEXT_FILE = u'generate_second_posts_lines.txt'

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

SKIP_LABELS = {'git', 'goal', 'discussion', 'TODO', 'wont fix', 'works for me',
               'rejected', 'duplicate'} | set(GAMES)

URL_MILESTONE = \
    'https://github.com/wrye-bash/wrye-bash/issues?milestone=%i&state=open'
URL_BUGS = 'https://github.com/wrye-bash/wrye-bash/issues?labels=bug'
URL_ENHANCEMENTS = \
    'https://github.com/wrye-bash/wrye-bash/issues?labels=enhancement'

COLOR_INTRO = 'orange'
COLOR_ASSIGNEE = '#00FF00'
COLOR_DONE = 'orange'


# Functions ===================================================================
def parseArgs():
    parser = argparse.ArgumentParser(prog='Generate Second Posts',
                                     add_help=True)
    parser.add_argument('-m', '--milestone',
                        dest='milestone',
                        action='store',
                        type=str,
                        required=True,
                        help='Specify the milestone for filtering Issues.')
    parser.add_argument('-u', '--user',
                        dest='user',
                        action='store_true',
                        default=False,
                        help='Force usage of a different user to pull info.')
    gameGroup = parser.add_mutually_exclusive_group()
    gameGroup.add_argument('-g', '--game',
                           dest='game',
                           type=str,
                           choices= ['skyrim',
                                     'oblivion',
                                     'fallout',
                                     'fnv',
                                     ],
                           help='Generate a second post for a specific game.')
    gameGroup.add_argument('-a', '--all',
                           dest='all',
                           action='store_true',
                           default=False,
                           help='Generate a second post for all games.')
    return parser.parse_args()


# writeSecondPost formatting functions ========================================
def color(text, color=None):
    if color:
        return '[color='+color+']' + text + '[/color]'
    else:
        return text

def url(url, title):
    return '[url='+url+']' + title + '[/url]'

def bold(text):
    return '[b]' + text + '[/b]'

def strike(text):
    return '[s]' + text + '[/s]'

def li(text):
    return '[*]' + text

def formatIssue(issue, issueType):
    if issue.state == 'open':
        s = lambda x: x
    else:
        s = lambda x: color(strike(x), COLOR_DONE)
    if issue.assignee:
        assignee = issue.assignee
        assignee = ' ' + url(assignee.url,
                             color('(' + assignee.login + ')', COLOR_ASSIGNEE))
    else:
        assignee = ''
    return li(s(url(issue.html_url, issueType + ' %i' % issue.number) +
                ': ' + issue.title)
              + assignee)


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
    if not os.path.exists(u'out'):
        os.makedirs(u'out')
    outFile = os.path.join(u'out',
                           u'Buglist thread Starter - ' + gameTitle + u'.txt')
    with open(outFile, 'w') as out:
        with open(TEXT_FILE,'r') as ins:
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


def main():
    """Start everything off"""
    # Figure out which games to do:
    opts = parseArgs()
    if opts.game:
        games = {opts.game: GAMES[opts.game]}
    else:
        games = GAMES
    # login
    if opts.user:
        user = getUser()
    else:
        user = (TOKEN,)
    print "Logging in..."
    git = getGithub(*user)
    print "User:", git.get_user().name
    print "Getting repository..."
    repo = getRepo(git, ORG_NAME, REPO_NAME)
    if not repo:
        print 'Could not find repository:', REPO_NAME
        return
    print "Getting Milestone..."
    milestone = getMilestone(repo, opts.milestone)
    if not milestone:
        print 'Could not find milestone:', opts.milestone
        return
    # Clean output directory
    if os.path.exists(u'out'):
        try:
            shutil.rmtree(u'out')
        except:
            pass
    # Create posts
    for game in games:
        print 'Getting Issues for:', games[game]
        issues = getIssues(repo, milestone, game)
        print 'Writing second post...'
        writeSecondPost(games[game], milestone, issues)
    print 'Second post(s) genterated.'

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Aborted"
