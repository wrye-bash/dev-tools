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

"""This module generates the changelog reading metadata for a milestone."""
import argparse
from datetime import date
from github_wrapper import getMilestone, getIssues
from globals import GAMES, _login, _cleanOutDir, _getRepo, _outFile

# Functions ===================================================================
def parseArgs():
    parser = argparse.ArgumentParser(prog='Generate Changelog',
                                     add_help=True)
    parser.add_argument('-m', '--milestone',
                        dest='milestone',
                        action='store',
                        type=str,
                        required=True,
                        help='Specify the milestone for latest release.')
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
                           help='Show issues for a specific game only.')
    gameGroup.add_argument('-a', '--all',
                           dest='all',
                           action='store_true',
                           default=False,
                           help='Show issues for all games.')
    return parser.parse_args()

TEMPLATE = u'changelog_template.txt'
from html import h2

def _title(milestone,authors=('Various community members',)):
    return h2(milestone.title + ' [' + date.today().strftime(
        '%Y/%m/%d') + '] [' + authors + ']'
    )

def writeChangelog(gameTitle, milestone):
    """Write 'Buglist thread Starter - <gameTitle>.txt'"""
    outFile = _outFile(name=u'Buglist thread Starter - ' + gameTitle + u'.txt')
    with open(outFile, 'w') as out:
        # with open(TEMPLATE,'r') as ins:
        out.write('\n'.join(_title(milestone)))
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
    opts = parseArgs()
    # Figure out which games to do:
    if opts.game:
        games = {opts.game: GAMES[opts.game]}
    else:
        games = GAMES
    # Login
    git = _login(opts)
    if not git: return
    repo = _getRepo(git)
    if not repo: return
    milestone = getMilestone(opts, repo)
    # Create posts
    for game in games:
        print 'Getting Issues for:', games[game]
        issues = getIssues(repo, milestone, game)
        print 'Writing changelog'
        writeChangelog(games[game], milestone, issues)
    print 'Changelog generated.'

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Aborted"
