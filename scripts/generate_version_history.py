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

"""This module generates the version history html for the readme based on the
changelog for a milestone. It then copies the Wrye Bash Version History.html to
 the wrye-bash and wrye-bash.github.io repositories which are supposed to lie
 on the parent directory of the dir this script is run from."""

from generate_changelog import writeChangelog
from globals import _template, Parser, _outFile, hub

TEMPLATE_HEAD = _template(name=u'Wrye Bash Version History - head.txt')
TEMPLATE_TAIL = _template(name=u'Wrye Bash Version History - tail.txt')

# Functions ===================================================================
def _parseArgs():
    return Parser.new(prog='Wrye Bash Version History.html').user().milestone(
        help_='Specify the milestone for latest release.').editor().parse()

import shutil
import os.path
import subprocess

# TODO command line args for those
WRYE_BASH_REPO_DOCS_DIR = 'wrye-bash\\Mopy\\Docs'
IO_REPO_DOCS_DIR = 'wrye-bash.github.io\\docs'

def writeVersionHistory(repo, milestone, editor):
    """Writes the html, copies it to the main repo and waits for you to
    manually edit it (and commit it) before it copies the edited file to the
    wrye-bash.github.io\\docs folder
    :param repo:
    :param milestone:
    """
    out_ = _outFile(name=u'Wrye Bash Version History.html')
    with open(out_, 'wb') as outfile:
        with open(TEMPLATE_HEAD) as readfile:
            shutil.copyfileobj(readfile, outfile)
        latestChangelog = writeChangelog(repo,
                                         milestone)  # TODO overwrite flag
        if editor:
            print('Please review the changelog (mind the date): ' + str(
                latestChangelog))
            subprocess.call([editor, str(latestChangelog)])  # TODO call_check
        with open(latestChangelog) as readfile:
            shutil.copyfileobj(readfile, outfile)
        with open(TEMPLATE_TAIL) as readfile:
            shutil.copyfileobj(readfile, outfile)
    if editor:
        print('Please review the html ' + str(out_))
        print(
            'It will then be copied to the main repository for you to commit')
        subprocess.call([editor, str(out_)])  # TODO call_check
    raw_input('Press Enter to copy the html to the main and io repos.')
    docsDir = os.path.join(os.path.abspath('../..'), WRYE_BASH_REPO_DOCS_DIR)
    print('Copying to ' + str(docsDir))
    shutil.copy(out_, docsDir)
    docsDir = os.path.join(os.path.abspath('../..'), IO_REPO_DOCS_DIR)
    # TODO: launch git gui & to inspect the diff - GitPython
    # TODO soft link instead of copying
    print('Copying to ' + str(docsDir))
    shutil.copy(out_, docsDir)

def main():
    opts = _parseArgs()
    if opts.no_editor:
        editor = None
    else:
        editor = opts.editor
    git_ = hub(opts)
    if not git_: return
    repo, milestone = git_[0], git_[1]
    writeVersionHistory(repo, milestone, editor)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Aborted"
