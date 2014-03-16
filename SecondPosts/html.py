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

"""This module exports formatting functions for the forums and the doc files we
use."""

COLOR_INTRO = 'orange'
COLOR_ASSIGNEE = '#00FF00'
COLOR_DONE = 'orange'

# BBCODE ========================================
def color(text,color_=None):
    if color_:
        return '[color=' + color_ + ']' + text + '[/color]'
    else:
        return text

def url(url_,title):
    return '[url=' + url_ + ']' + title + '[/url]'

def bold(text):
    return '[b]' + text + '[/b]'

def strike(text):
    return '[s]' + text + '[/s]'

def li(text):
    return '[*]' + text

def formatIssue(issue,issueType):
    if issue.state == 'open':
        s = lambda x: x
    else:
        s = lambda x: color(strike(x),COLOR_DONE)
    if issue.assignee:
        assignee = issue.assignee
        assignee = ' ' + url(assignee.url,
            color('(' + assignee.login + ')',COLOR_ASSIGNEE))
    else:
        assignee = ''
    return li(s(url(issue.html_url,issueType + ' %i' % issue.number) +
                ': ' + issue.title)
              + assignee)

# HTML ========================================
def h2(text):
    return '<h2>' + text + '</h2>'

def ul(items,f=lambda x: x):
    yield '<ul>'
    for i in items:
        yield '\t<li>' + f(i) + '</li>'
    yield '</ul>'

def closedIssue(issue):
    """Description of a closed issue"""
    if issue.assignee:
        assignee = issue.assignee
        assignee = ' ' + '[' + assignee.login + ']'
    else:
        assignee = ''
    return issue.title + assignee
