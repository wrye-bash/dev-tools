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

"""This module generates the first posts for the Bethesda forums threads. Uses
a common template for Oblivion and Skyrim posts which is not yet set in
stone. Some manual editing may be needed (pay attention to the latest release
date and thread links). Also unicode and newlines support is very much a
hack."""

# Functions ===================================================================
from generate_changelog import writeChangelogBBcode
from globals import templatePath, GAMES
import cli_parser

def _parseArgs():
    return cli_parser.Parser(
        description='Generate first posts for Bethesda forums').milestone(
        help_='Specify the milestone for latest release.').editor(
    ).parse()

POSTS_DIR = '../FirstPosts'
TEMPLATE = templatePath(name=u'generate_first_posts_lines.txt')

def _previous_thread(game):
    return 'Continuing from the [topic=' + str(
        game.prev_thread) + ']previous thread[/topic]...'

def _thread_history(game):
    if game == 'skyrim':
        with open(templatePath(name="Thread History.txt"), "r") as threads:
            return threads.read()

def _other_threads(label):
    for gameName, game in GAMES.iteritems():
        if gameName != label:
            yield ('[*]The Official [topic=' + str(game.cur_thread) +
                   ']Wrye Bash for ' + game.display + ' thread[/topic].[/*]')

import subprocess
import string
from globals import outPath

def writeFirstPosts(milestone, editor):
    for label, game in GAMES.iteritems():
        out_ = outPath(dir_=POSTS_DIR,
                        name=u'Forum thread starter - ' + game.display +
                             u'.txt')
        print out_
        with open(out_, 'w') as out:
            out.write(_previous_thread(game))
            out.write('\n\n')
            history = _thread_history(label)
            if history:
                out.write(history)
            with open(TEMPLATE, 'r') as template:
                data = template.read()  # reads file at once - should be OK
            data = data.decode('utf-8')  # NEEDED
            src = string.Template(data)
            with open(writeChangelogBBcode(None, milestone),
                      'r') as changelog_file:
                changelog = changelog_file.read()
                changelog = changelog.decode('utf-8')  # just in case changelog
                # contains unicode chars  # reads file at once - should be OK
            dictionary = {'game': game.display, 'nexus_url': game.nexusUrl,
                          'game_threads': '\n'.join(_other_threads(label)),
                          'latest_changelog': changelog}
            src_substitute = src.substitute(dictionary)
            src_substitute = src_substitute.encode('utf-8')  # NEEDED
            out.write(src_substitute)
        if editor:
            print('Please review (mind the release date and thread links):'
                  + str(out.name))
            subprocess.call([editor, out.name])  # TODO call_check

def main():
    opts = _parseArgs()
    if opts.no_editor:
        editor = None
    else:
        editor = opts.editor
    writeFirstPosts(opts.milestone, editor)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Aborted"
