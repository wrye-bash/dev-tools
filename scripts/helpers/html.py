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

"""This module exports formatting functions for the forums and the doc files we
are generating."""

# MARKDOWN ========================================
def markdownList(items, f=lambda x: x):
    for i in items:
        yield '- ' + f(i)

# BBCODE ========================================
def color(colour, text):
    if colour:
        return '[color=' + colour + ']' + text + '[/color]'
    else:
        return text

def font(daFont, text):
    return '[font=' + daFont + ']' + text + '[/font]'

def url(url_, title):
    return '[url=' + url_ + ']' + title + '[/url]'

def bold(text):
    return '[b]' + text + '[/b]'

def center(text):
    return '[center]' + text + '[/center]'

def strike(text):
    return '[s]' + text + '[/s]'

def li(text):
    return '[*]' + text + '[/*]'

def bbList(items, f=lambda x: x, *args):
    yield '[LIST]'
    if not args:
        for i in items:
            yield li(f(i))
    else:
        for i in items:
            yield li(f(i, *args))
    yield '[/LIST]'

def spoiler(text):
    yield '[spoiler]'
    yield text
    yield '[/spoiler]'

def size(num, text):
    return '[size=' + str(num) + ']' + text + '[/size]'

# HTML ========================================
def h3(text):
    return '<h3>' + text + '</h3>'

def ul(items, f=lambda x: x):
    yield '\n<ul>'
    for i in items:
        yield '<li>' + f(i) + '</li>'
    yield '</ul>'

def closedIssue(issue):
    """String representation of a closed issue with assignee."""
    if issue.assignee:
        assignee = issue.assignee
        assignee = ' ' + '[' + assignee.login + ']'
    else:
        assignee = ''
    return issue.title + assignee
