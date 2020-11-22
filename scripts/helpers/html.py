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

from collections import OrderedDict

# MARKDOWN ========================================
def markdown_list(items, f=lambda x: x):
    for i in items:
        yield u'- ' + f(i)

def markdown_link(text, href):
    return u'[%s](%s)' % (text, href)

# https://www.markdownguide.org/basic-syntax/#escaping-characters
_md_escapes = OrderedDict([
    (u'\\', u'\\\\'),
    (u'`',  u'\\`'),
    (u'*',  u'\\*'),
    (u'_',  u'\\_'),
    (u'{',  u'\\{'),
    (u'}',  u'\\}'),
    (u'[',  u'\\['),
    (u']',  u'\\]'),
    (u'(',  u'\\('),
    (u')',  u'\\)'),
    (u'#',  u'\\#'),
    (u'+',  u'\\+'),
    (u'-',  u'\\-'),
    (u'.',  u'\\.'),
    (u'!',  u'\\!'),
    (u'|',  u'\\|'),
])

def markdown_escape(text):
    for target, sub in _md_escapes.iteritems():
        text = text.replace(target, sub)
    return text

# BBCODE ========================================
def li(text):
    return u'[*]' + text + u'[/*]'

def bb_list(items):
    yield u'[LIST]'
    for i in items:
        yield li(i)
    yield u'[/LIST]'

def spoiler(text):
    yield u'[spoiler]'
    yield text
    yield u'[/spoiler]'

def size(num, text):
    return u'[size=' + str(num) + u']' + text + u'[/size]'

# HTML ========================================
def h3(text):
    return u'<h3>' + text + u'</h3>'

def ul(items, f=lambda x: x):
    yield u'\n<ul>'
    for i in items:
        yield u'<li>' + f(i) + u'</li>'
    yield u'</ul>'

def a(text, href):
    return u'<a href="%s">%s</a>' % (href, text)

def closed_issue(issue):
    """String representation of a closed issue with assignee."""
    assignees = u''
    if issue.assignees:
        assignees = u' [%s]' % u', '.join(
            sorted(assignee.login for assignee in issue.assignees))
    return u'#%u: ' % issue.number + issue.title + assignees
