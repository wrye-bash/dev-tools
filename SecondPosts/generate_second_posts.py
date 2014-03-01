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

   Requires a username/password or access token to get the information, I have
   not been able to use the github API without having it first log on.  See
   the wiki on wrye-bash/meta on setting up a access token (highly recommened).

   Generated seconds posts will be output to ./out
   """


# Imports ====================================================================
import argparse
import sys
import os


import github


# Globals ====================================================================
USER_FILE = u'generate_second_posts.usr'
TEXT_FILE = u'generate_second_posts_lines.txt'

REPO_NAME = u'wrye-bash'
ORG_NAME = u'Wrye Bash'

GAMES = {
    # Convert to display names
    'skyrim': u'Skyrim',
    'oblivion': u'Oblivion',
    'fallout': u'Fallout 3',
    'fnv': u'Fallout - New Vegas',
    }

SKIP_LABELS = {'git', 'goal', 'discussion', 'TODO', 'wont fix', 'works for me',
               'rejected', 'duplicate'} | set(GAMES)

COLOR_INTRO = 'orange'
COLOR_ASSIGNEE = '#FFA500'
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


def getUser():
    """Attempts to load 'generate_second_posts.user' to read in user data for
       accessing GitHub API.  If the file is not present or the data invalid,
       prompts the user to input his or her data, and asks if it should be
       saved.
         Return: tuple either of:
             (username, password) - without 2 factor authentication
             (key,) - with 2 factor authentication
    """
    user = None
    password = None
    key = None
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE) as ins:
                lines = ins.readlines()
            # filter out empty lines
            lines = [line.strip() for line in lines if line and line.strip()]
            if len(lines) == 1:
                # 2-factor authentication
                key = lines[0]
            elif len(lines) == 2:
                user, password = lines
        except:
            pass
    if (not user or not password) and (not key):
        # Invalid, prompt for input
        print ("User settings file missing or invalid data present.  Please "
               "input your information.  If you are using 2-factor"
               "authentication on your account, please see our Wiki page on "
               "setting up a Personal Access Token for this script.")
        print " 1) Entering a Personal Access Token"
        print " 2) Entering a user name and password"
        print " 3) Exit"
        input = raw_input(">")
        if input == '1':
            user = raw_input('user:')
            password = raw_input('password:')
        elif input == '2':
            key = raw_input('token:')
        else:
            return ()
        print
        save = raw_input("Would you like to save these settings to the user "
                         "settings file? [Y/N]:")
        if save in ('y','Y'):
            with open(USER_FILE, 'w') as out:
                if key:
                    out.write(key)
                else:
                    out.write(user)
                    out.write('\n')
                    out.write(password)
    if key:
        return (key,)
    return (user, password)


def getRepo(git, orgName, repoName):
    """Get a githubapi repository object for the specified repository.
        git: github.Github object for the user
        orgName: display name of the orginizations for the repository
                 (not the link name, ie Wrye Bash is the name, but
                  wrye-bash is the link to access it).  If orgName is
                  None, assumes personal repos.
        repoName: name of the repository to get
    """
    if orgName:
        for org in git.get_user().get_orgs():
            if org.name == orgName:
                for repo in org.get_repos():
                    if repo.name == repoName:
                        return repo
    else:
        for repo in git.get_user().get_repos():
            if repo.name == repoName:
                return repo
    return None


def getMilestone(repo, milestone):
    """Returns the github.Milestone object for a specified milstone."""
    for m in repo.get_milestones():
        if m.title == milestone:
            return m
    return None


def getIssues(repo, milestone, gameLabel):
    """Return a tuple of applicable issues for the given game and milestone
        repo: github.Repository object
        milestone: github.Milestone object
        gameLabel: label for the specific game (ie: `skyrim`, `fnv`, etc)
       return:
        (current_bug, current_enh, other_bug, other_enh)
        where:
          current_bug: Issues tagged `bug` for milestone
          current_enh: Issues tagged `enhancement` for milestone
          other_bug: Issues tagged `bug`, but not for this milestone
          other_enh: Issues tagged `enhancement`, but not for this milestone
        Some Issues will be filtered out, regardless, such as those tagged with
        `git`, etc."""
    current = repo.get_issues(milestone,
                              state='all',
                              sort='created',
                              direction='desc')
    other = repo.get_issues(state='open',
                            sort='created',
                            direction='desc')
    skip_labels = SKIP_LABELS - {gameLabel}
    # Filter current issues
    current_bug = []
    current_enh = []
    for issue in current:
        labels = set(x.name for x in issue.get_labels())
        if skip_labels & labels:
            # Has one of the labels we're skipping
            continue
        if 'bug' in labels:
            current_bug.append(issue)
        elif 'enhancement' in labels:
            current_enh.append(issue)
    # Filter other issues
    other_bug = []
    other_enh = []
    for issue in other:
        if issue.state != 'open':
            # Only care about open issues...
            continue
        if issue.milestone and issue.milestone.title == milestone.title:
            # ...and issues that aren't part of the milestone.
            continue
        labels = set(x.name for x in issue.get_labels())
        if skip_labels & labels:
            continue
        if 'bug' in labels:
            other_bug.append(issue)
        elif 'enhancement' in labels:
            other_enh.append(issue)
    # Sort current_bug/enh: already sorted by date, just move the
    #  open issues to the top
    current_bug = ([x for x in current_bug if x.state == 'open'] +
                   [x for x in current_bug if x.state == 'closed'])
    return (current_bug, current_enh, other_bug, other_enh)


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
        assignee = ' ' + color(issue.assignee.name, COLOR_ASSIGNEE)
    else:
        assignee = ''
    return li(s(url(issue.html_url, issueType + ' %i' % issue.id) +
                ': ' + issue.title)
              + assignee)


def writeSecondPost(gameTitle, milestone, issues):
    """Write 'Buglist thread Starter - <gameTitle>.txt'"""
    os.makedirs(u'out')
    with open(u'out\\Buglist thread Starter - ' + gameTitle + u'.txt', 'w') as out:
        with open(TEXT_FILE,'r') as ins:
            # Intro paragraph
            line = ins.readline().strip('\r\n')
            out.write(color(line % milestone.title, COLOR_INTRO))
            out.write(ins.readline())
            out.write('\n')
            # Upcoming release
            line = ins.readline().strip('\r\n')
            out.write(url('https://github.com/wrye-bash/wrye-bash/issues?milestone=%i&state=open' % milestone.id,
                          line % milestone.title))
            out.write('\n[list]\n')
            for issueList,issueType in ((issues[0],'Bug'),
                                        (issues[1],'Enhancement')):
                for issue in issueList:
                    out.write(formatIssue(issue, issueType))
                    out.write('\n')
            out.write('[/list]\n\n')
            # Other known bugs
            out.write(url('https://github.com/wrye-bash/wrye-bash/issues?state=open',
                          'Additional known bugs:\n'))
            out.write('[spoiler][list]\n')
            for issue in issues[2]:
                out.write(formatIssue(issue, 'Bug'))
                out.write('\n')
            if not issues[2]:
                out.write('None')
            out.write('[/list][/spoiler]\n\n')
            # Other known feature requests
            out.write((url('https://github.com/wrye-bash/wrye-bash/issues?state=open',
                           'Additional requested features:\n')))
            out.write('[spoiler][list]\n')
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
    user = getUser()
    print "Logging in..."
    git = github.Github(*user)
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
    for game in games:
        print 'Getting Issues for:', games[game]
        issues = getIssues(repo, milestone, game)
        print 'Writing second post...'
        writeSecondPost(games[game], milestone, issues)
    print 'Second post(s) genterated.'

if __name__ == '__main__':
    main()
