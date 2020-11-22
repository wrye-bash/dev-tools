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
from __future__ import absolute_import, print_function

import os.path
import subprocess
from datetime import date
from functools import partial
from html import escape as html_escape

import github_login
from cli_parser import Parser
from helpers.html import h3, ul, bb_list, size, markdown_list, spoiler, a, \
    markdown_link, markdown_escape, closed_issue
from helpers.github_wrapper import get_closed_issues
from globals import out_path, DEFAULT_MILESTONE_TITLE

CHANGELOG_TITLE_SIZE = 5

# Functions ===================================================================
def _parse_args():
    return Parser(description=u'Generate Changelog').editor().milestone(
        help_=u'Specify the milestone for latest release.').authors(
    ).offline().overwrite().milestone_title().parse()

def _title(title, authors=None):
    title = title + u'[' + date.today().strftime(u'%Y/%m/%d') + u']'
    if not authors: return title
    return title + u' [' + u', '.join(authors) + u']'

def _changelog_bbcode(issues, title, out_file):
    with open(out_file, u'w') as out:
        out.write(size(CHANGELOG_TITLE_SIZE, _title(title)))
        out.write(u'\n'.join(spoiler('\n'.join(bb_list(issues)))))
        out.write(u'\n')
    return out_file

def _changelog_txt(issues, title, out_file):
    issue_template = u'https://github.com/wrye-bash/wrye-bash/issues/%u'
    def add_link(issue_line):
        issue_num, issue_rest = issue_line.split(u':', 1)
        issue_link = a(issue_num, href=issue_template % int(issue_num[1:]))
        return issue_link + u':' + html_escape(issue_rest)
    with open(out_file, u'w') as out:
        out.write(h3(html_escape(_title(title))))
        out.write(u'\n'.join(ul(issues, f=add_link)))
        out.write(u'\n\n')  # needs blank line for Version History.html
    return out_file

def _changelog_markdown(issues, title, out_file):
    issue_template = u'https://github.com/wrye-bash/wrye-bash/issues/%u'
    def add_link(issue_line):
        issue_num, issue_rest = issue_line.split(u':', 1)
        issue_link = markdown_link(issue_num,
            href=issue_template % int(issue_num[1:]))
        return issue_link + u':' + markdown_escape(issue_rest)
    with open(out_file, u'w') as out:
        out.write(markdown_escape(_title(title)))
        out.write(u'\n\n')
        out.write(u'\n'.join(markdown_list(issues, f=add_link)))
        out.write(u'\n')
    return out_file

# API =========================================================================
CHANGELOGS_DIR = os.path.join(os.getcwdu(), u'ChangeLogs')
print(u'Current working directory is %s' % os.getcwdu())
print(u'Changelogs will be placed in %s' % CHANGELOGS_DIR)

def write_changelog(issue_list, num, title=DEFAULT_MILESTONE_TITLE,
        overwrite=False, extension=u'.txt', logic=_changelog_txt):
    """Write 'Changelog - <milestone>.txt'"""
    if issue_list is None:
        issue_list, _ = __get_issue_list(num)
    out_file = out_path(dir_=CHANGELOGS_DIR,
        name=u'Changelog - ' + num + extension)
    print(out_file)
    if os.path.isfile(out_file) and not overwrite: return out_file
    title = num + u' ' + title + u' ' if title else num
    return logic(issue_list, title, out_file)

def write_changelog_bbcode(issue_list, num, title=DEFAULT_MILESTONE_TITLE,
        overwrite=False):
    """Write 'Changelog - <milestone>.bbcode.txt'"""
    return write_changelog(issue_list, num, title, overwrite,
        extension=u'.bbcode.txt', logic=_changelog_bbcode)

def write_changelog_markdown(issue_list, num, title=DEFAULT_MILESTONE_TITLE,
        overwrite=False):
    """Write 'Changelog - <milestone>.markdown.txt'"""
    return write_changelog(issue_list, num, title, overwrite, extension=u'.md',
        logic=_changelog_markdown)

def main():
    opts = _parse_args()  # TODO per game # if opts.game:...
    issue_list, milestone = __get_issue_list(
        opts.milestone, opts.editor, opts if not opts.offline else None)
    if issue_list is None: return
    num = milestone.title if milestone else opts.milestone
    print(u'Writing changelogs')
    globals()['_title'] = partial(_title, authors=(opts.authors.split(u',')))
    write_changelog(issue_list, num, opts.title, opts.overwrite)
    write_changelog_markdown(issue_list, num, opts.title, opts.overwrite)
    write_changelog_bbcode(issue_list, num, opts.title, opts.overwrite)
    print(u'Changelogs generated.')

def __get_issue_list(miles_num, editor=None, opts=None):
    issue_list = milestone = None
    issue_list_txt = u'issue_list.' + miles_num + u'.txt'
    if opts: # get the issues from github and save them in a text file
        git_ = github_login.hub(miles_num)
        if git_ is not None:
            repo, milestone = git_[0], git_[1]
            issues = get_closed_issues(repo, milestone)
            issue_list = map(closed_issue, issues)
            issue_list = _dump_plain_issue_list(editor, issue_list,
                issue_list_txt)
    else: # work offline, if it blows on you you get a black star for not RTM
        issue_list = _read_plain_issue_list(issue_list_txt)
        # print issue_list
    return issue_list, milestone

def _dump_plain_issue_list(editor, issue_list, txt_):
    with open(out_path(dir_=CHANGELOGS_DIR, name=txt_), u'w') as out:
        out.write(u'\n'.join(issue_list))
    if editor:
        print(u'Please edit the issues as you want them to appear on '
              u'the changelogs:' + unicode(out.name))
        subprocess.call([editor, out.name])  # TODO block
        _ = raw_input(u'Press enter when done>')
        issue_list = _read_plain_issue_list(txt_)
    return issue_list

def _read_plain_issue_list(txt_):
    with open(out_path(dir_=CHANGELOGS_DIR, name=txt_), u'r') as in_:
        return in_.read().splitlines()

if __name__ == u'__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(u'Aborted')
