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

"""This module generates the Nexus description text. Uses
a common template for Oblivion and Skyrim posts which is not yet set in
stone. Some manual editing may be needed (pay attention to the latest release
date and thread links). Also unicode and newlines support is very much a
hack."""

# Functions ===================================================================
from generate_changelog import writeChangelogBBcode
from globals import templatePath, GAMES
from helpers.html import center, size, color, font
import cli_parser

def _parseArgs():
    return cli_parser.Parser(
        description='Generate Nexus description text').milestone(
        help_='Specify the milestone for latest release.').editor(
    ).parse()

NEXUS_DIR = '../NexusDescriptionPages'
TEMPLATE = templatePath(name=u'generate_nexus_description_lines.txt')

def _we_only_support(game):
    return center(color('red', size(6, 'We only support ' + game.display +
        ' version ' + game.patch + '+ and\nWrye Bash %s or higher.'
                                    % game.minimum_bash_version)))

def _what_bash_does(label):
    bullets = """\n\n[list]\n"""
    bullets += (
        '[*]It makes it safe to try out new mods because it will restore '
        'everything to the way it was when you uninstall a mod\n'
        '[*]It makes more mods compatible with each other by importing '
        'information from different mods into a "bashed patch"\n')
    if label == 'oblivion': bullets += "[*]It allows you to exceed the 255" + \
    " mod threshold by automatically merging mods for you\n"
    bullets += """[/list]"""
    return bullets

def _beth_url(num):
    return 'http://forums.bethsoft.com/topic/%s-/' % str(num)

def _beta_headsup(beta='307.beta1',
                  _obThread=_beth_url(GAMES['oblivion'].cur_thread)):
    return center(font('Comic Sans MS', size(4,
        color('#ff00ff', "%s is out ! Please post feedback on the official ")
                                             % beta +
        color('#9900ff', "[url=%s]Oblivion thread[/url]" % _obThread))))

def _beth_thread():
    threads = ['[url=%s]%s[/url]' % (_beth_url(g.cur_thread), g.display)
               for g in GAMES.values() if g.cur_thread]
    return ', '.join(threads)

import subprocess
import string
from globals import outPath
import re

# http://stackoverflow.com/a/6117124/281545 - hack to convert changelog format
rep = {'[spoiler]': "", '[/spoiler]': "", "size=5": "color=#00BFFF",
       "/size": '/color'}
rep = dict((re.escape(k), v) for k, v in rep.iteritems())
_patternAny = re.compile("|".join(rep.keys()), flags=re.I)
def _unspoil(text):
    return _patternAny.sub(lambda m: rep[re.escape(m.group(0))], text)

def writeNexusDescription(num, editor):
    for label, game in GAMES.iteritems():
        out_ = outPath(dir_=NEXUS_DIR,
                       name=u'Nexus - ' + game.display + u' Wrye Bash.txt')
        print out_
        with open(out_, 'w') as out:
            out.write(_we_only_support(game))
            out.write('\n\n')
            with open(TEMPLATE, 'r') as template:
                data = template.read()  # reads file at once - should be OK
            data = data.decode('utf-8')  # NEEDED
            src = string.Template(data)
            with open(writeChangelogBBcode(None, num, overwrite=False),
                      'r') as changelog_file:
                changelog = changelog_file.read() # reads file at once
                changelog = _unspoil(changelog).strip()
                changelog = changelog.decode('utf-8')  # just in case changelog
                # contains unicode chars
            notes = game.game_nexus_notes
            game_notes = notes if not notes else '\n' + notes + '\n'
            dictionary = {'game': game.display,
                          'game_notes': game_notes,
                          'what_bash_does': _what_bash_does(label),
                          'latest_changelog': changelog,
                          'beth_thread': _beth_thread(),
                          'beta_headsup': _beta_headsup(),
                          }
            src_substitute = src.substitute(dictionary)
            src_substitute = src_substitute.encode('utf-8')  # NEEDED
            out.write(src_substitute)
        if editor:
            print('Please review (mind the release date and thread links):'
                  + str(out.name))
            subprocess.call([editor, out.name])  # TODO call_check

def main():
    opts = _parseArgs()
    writeNexusDescription(opts.milestone, opts.editor)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Aborted"
