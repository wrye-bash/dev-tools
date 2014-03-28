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
import os

USER_FILE = u'generate_second_posts.usr'
DEFAULT_ISSUE_STATE = 'all'
DEFAULT_MILESTONE = None

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

class _IssueCache(object):
    CACHE = {}
    ALL_LABELS = {}

    class IssueFilter(object):
        def __init__(self, repo, milestone, state):
            self.repo = repo
            self.milestone = milestone
            self._state = state

        @property
        def state(self):
            return self._state

        @state.setter
        def state(self, value): # disallow None
            if not value:
                self._state = DEFAULT_ISSUE_STATE
            else:
                self._state = value

        def __key(self): # http://stackoverflow.com/a/2909119/281545
            return self.repo, self.milestone, self.state

        def __eq__(self, other):  # copy paste
            return type(other) is type(self) and self.__key() == other.__key()

        def __hash__(self): return hash(self.__key())

    @staticmethod
    def hit(repo, milestone, state):
        issueFilter = _IssueCache.IssueFilter(repo, milestone, state)
        return _IssueCache.CACHE.get(issueFilter)

    @staticmethod
    def update(repo, milestone, state, issues):  # not thread safe
        issueFilter = _IssueCache.IssueFilter(repo, milestone, state)
        _IssueCache.CACHE[issueFilter] = issues

    @staticmethod
    def all(repo, milestone=None, state=DEFAULT_ISSUE_STATE):
        issueFilter = _IssueCache.IssueFilter(repo, milestone, state)
        all_ = _IssueCache.ALL_LABELS.get(issueFilter)
        if not all_:
            if milestone:  # FIXME milestone=github.GithubObject.NotSet ...
                all_ = _IssueCache.ALL_LABELS[issueFilter] = repo.get_labels(
                    milestone, state)
            else:
                all_ = _IssueCache.ALL_LABELS[issueFilter] = repo.get_labels(
                    state)
        return all_

def getIssues(repo, milestone=None, keep_labels=None, skip_labels=(),
              state=DEFAULT_ISSUE_STATE):
    """Return a _list_ of applicable issues for the given game and milestone
        repo: github.Repository object
        milestone: github.Milestone object
        keep_labels: set of labels an issue must partake to, to be included
          in the results - by default all labels including no labels at all
        skip_labels: set of labels to skip, by default empty - if an issue
         has labels in this set it will be skipped
        state: open or closed - by default 'all'
       return: a list of issues
        :rtype: :class:`github.PaginatedList.PaginatedList` of
        :class:`github.Issue.Issue`
    TODO: add sort, direction as needed, clean ifs up, list comprehensions
    """
    print skip_labels
    current = _IssueCache.hit(repo, milestone, state)
    if not current:
        print repo, milestone, state
        if milestone: # FIXME - due to API won't let me specify None for all
            current = repo.get_issues(milestone,
                                      state=state,
                                      sort='created',
                                      direction='desc')
        else:
            current = repo.get_issues(state=state,
                                      sort='created',
                                      direction='desc')
        _IssueCache.update(repo, milestone, state, current)
    if not keep_labels and not skip_labels:  # no label filters, return All
        return current
    # return only issues that partake in keep_labels, and not in skip_labels
    result = []
    if not keep_labels and skip_labels:
        for issue in current:
            labels = set(x.name for x in issue.labels)
            if not skip_labels & labels:
                result.append(issue)
        return result
    elif keep_labels and skip_labels:
        keep_labels = keep_labels - skip_labels
        print current
        print keep_labels
        for issue in current:
            labels = set(x.name for x in issue.labels)
            if keep_labels & labels and not skip_labels & labels:
                result.append(issue)
        return result
    else:
        for issue in current:
            labels = set(x.name for x in issue.labels)
            if keep_labels & labels:
                result.append(issue)
        return result

def getUnlabeledIssues(repo, milestone=None, state=DEFAULT_ISSUE_STATE):
    return getIssues(repo, milestone, state=state,
                     skip_labels=_IssueCache.all(repo, milestone, state))

def getClosedIssues(repo, milestone, keep_labels={'bug', 'enhancement'}
                    # , gameLabel=None, skip_labels=set() # TODO, game, skip
):
    """Return a list of closed issues for the given milestone
        repo: github.Repository object
        milestone: github.Milestone object
        keep_labels: set of labels for result to partake
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
        labels = set(x.name for x in issue.labels)
        if keep_labels & labels:
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
