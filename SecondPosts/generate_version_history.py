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
from globals import _template, Parser, _login, _getRepo, _getMiles, _outFile

TEMPLATE_HEAD = _template(name=u'Wrye Bash Version History - head.txt')
TEMPLATE_TAIL = _template(name=u'Wrye Bash Version History - tail.txt')

# Functions ===================================================================
def _parseArgs():
    return Parser.new(prog='Wrye Bash Version History.html').user().milestone(
        help_='Specify the milestone for latest release.').parse()

import shutil
import os
WRYE_BASH_REPO_DOCS_DIR='wrye-bash\\Mopy\\Docs'
IO_REPO_DOCS_DIR='wrye-bash.github.io\\docs'

def writeVersionHistory(repo, milestone):
    """Writes the html, copies it to the main repo and waits for you to
    manually edit it before it copies the edited file to the 'wrye-bash
    .github.io\\docs' folder
    :param repo:
    :param milestone:
    """
    out_ = _outFile(name=u'Wrye Bash Version History.html')
    with open(out_, 'wb') as outfile:
        with open(TEMPLATE_HEAD) as readfile:
            shutil.copyfileobj(readfile, outfile)
        latestChangelog = writeChangelog(repo, milestone)
        with open(latestChangelog) as readfile:
            shutil.copyfileobj(readfile, outfile)
        with open(TEMPLATE_TAIL) as readfile:
            shutil.copyfileobj(readfile, outfile)
    docsDir = os.path.join(os.path.abspath('../..'), WRYE_BASH_REPO_DOCS_DIR)
    shutil.copy(out_, docsDir)
    htmlInDocs = os.path.join(docsDir, os.path.basename(out_))
    print('Hand edit ' + str(htmlInDocs))
    docsDir = os.path.join(os.path.abspath('../..'), IO_REPO_DOCS_DIR)
    # in_ =
    raw_input('Then press Enter to copy this file to ' + str(docsDir))
    # TODO soft link instead of copying + get the input
    shutil.copy(htmlInDocs, docsDir)

def main():
    opts = _parseArgs()
    # Login
    git = _login(opts)
    if not git: return
    repo = _getRepo(git)
    if not repo: return
    milestone = _getMiles(opts, repo)
    if not milestone: return
    writeVersionHistory(repo, milestone)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Aborted"

