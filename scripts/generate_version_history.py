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

"""This module generates the version history html for the readme based on the
changelog for a milestone. It then copies the Wrye Bash Version History.html to
 the wrye-bash and wrye-bash.github.io repositories which are supposed to lie
 on the parent directory of the dir this script is run from."""

from generate_changelog import writeChangelog
from globals import outPath
from cli_parser import Parser

# Functions ===================================================================
def _parseArgs():
    return Parser(
        description='Generate Wrye Bash Version History.html').milestone(
        help_='Specify the milestone for latest release.').editor().parse()

import shutil
import os.path
import subprocess

# TODO command line args for those
WRYE_BASH_REPO_DOCS_DIR = os.path.join(u'wrye-bash', u'Mopy', u'Docs')
IO_REPO_DOCS_DIR = os.path.join(u'wrye-bash.github.io', u'docs')

def writeVersionHistory(milestone, editor):
    """Writes the html, copies it to the main repo and waits for you to
    manually edit it (and commit it) before it copies the edited file to the
    wrye-bash.github.io\\docs folder
    :param milestone:
    """
    ## TODO: Currently this just copies the current version history
    ## from the user's local repo.  For a more reliable method, we
    ## can get the recent version from git itself.
    localSrc = u'Wrye Bash Version History.html'
    mainSrc = os.path.join(u'..', u'..',
                           WRYE_BASH_REPO_DOCS_DIR,
                           localSrc)
    out_ = outPath(name=localSrc)
    copied = False
    if not os.path.isfile(mainSrc):
        print('Wrye Bash Version History.html not found in the wrye-bash '
              'repository.  Please copy it to '
              'meta/scripts/Wrye Bash VersionHistory.html for editing.')
        raw_input('Press Enter when ready to continue')
    else:
        if os.path.isfile(localSrc):
            os.remove(localSrc)
        shutil.copy(mainSrc, localSrc)
        copied = True
    if not os.path.isfile(localSrc):
        print('Wrye Bash Version History.html is not present for editing.'
              '  The new changelog will be inserted into it.')
        return
    latestChangelog = writeChangelog(None, milestone)
    if editor:
        print('Please review the changelog (mind the date): '
              + str(latestChangelog))
        subprocess.call([editor, str(latestChangelog)])  # TODO call_check
    # Write new HTML with inserted changelog
    inserted = False
    with open(localSrc, 'rb') as ins:
        with open(out_, 'wb') as outfile:
            for line in ins:
                line = unicode(line, 'utf-8')
                if not inserted and line.strip().startswith(u'<h2>'):
                    # Found the start of the first version, insert our new
                    # changelog here
                    with open(latestChangelog) as readfile:
                        shutil.copyfileobj(readfile, outfile)
                    outfile.write(u'\n')
                    inserted = True
                outfile.write(line)
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
    if copied:
        os.remove(localSrc)

def main():
    opts = _parseArgs()
    if opts.no_editor:
        editor = None
    else:
        editor = opts.editor
    writeVersionHistory(opts.milestone, editor)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Aborted"
