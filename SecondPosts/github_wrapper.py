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

"""This module wraps github API calls."""

import github
from github import GithubException
import os

USER_FILE = u'generate_second_posts.usr'

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
        if save in ('y', 'Y'):
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
    # Try repos in organizations you're in
    if orgName:
        for org in git.get_user().get_orgs():
            if org.name == orgName:
                for repo in org.get_repos():
                    if repo.name == repoName:
                        print "Got repository from", orgName, "organization."
                        return repo
    # Try repos you own
    else:
        for repo in git.get_user().get_repos():
            if repo.name == repoName:
                print "Got repository from personal account."
                return repo
    # Try starred repos
    for repo in git.get_user().get_starred():
        if repo.name == repoName:
            print "Got repository from starred repositories."
            return repo
    # Try watched repos
    for repo in git.get_user().get_watched():
        if repo.name == repoName:
            print "Got repository from watched repositories."
            return repo
    return None


def getMilestone(repo, milestoneTitle):
    """Returns the github.Milestone object for a specified milestone."""
    for m in repo.get_milestones():
        if m.title == milestoneTitle:
            return m
    return None

# TODO builder for issues Issues.Builder.getIssues(repo).milestone(miles).
#   labels({'bug',enchancement'}).skip(GAMES - {game}).list()
def getIssues(repo, milestone, gameLabel, skip_labels=()):
    """Return a tuple of applicable issues for the given game and milestone
        repo: github.Repository object
        milestone: github.Milestone object
        gameLabel: label for the specific game (ie: `skyrim`, `fnv`, etc)
        skip_labels: set of labels to skip, by default empty
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
    skip_labels = skip_labels - {gameLabel}
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
    return current_bug, current_enh, other_bug, other_enh

def getClosedIssues(repo, milestone, accepted_labels = {'bug','enhancement'}
                    # , gameLabel=None, skip_labels=set() # TODO, game, skip
):
    """Return a list of closed issues for the given milestone
        repo: github.Repository object
        milestone: github.Milestone object
        accepted_labels: set of labels for result to partake
       return:
        issue fixed in this milestone."""
    current = repo.get_issues(milestone,
                              state='closed',
                              sort='created',
                              direction='desc')
    # if gameLabel is not None:
    #     skip_labels = skip_labels - {gameLabel}
    #     accepted_labels = accepted_labels | {gameLabel}
    # Filter current issues
    bug_or_enhancement = []
    for issue in current:
        labels = set(x.name for x in issue.get_labels())
        if  accepted_labels & labels:
            bug_or_enhancement.append(issue)
    return bug_or_enhancement

def getGithub(*user):
    return github.Github(*user)


def getUserName(git):
    try:
        return git.get_user().name
    except github.BadCredentialsException as e:
        raise GithubApiException(e.message)

class GithubApiException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)
        self.message = message
