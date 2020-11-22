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

"""This module exports global constants for the scripts that generate the
posts. Those constants are special to the wrye-bash/wrye-bash repository. If
the scripts are to be used for other repos too we need a repo factory here."""

import os

REPO_NAME = u'wrye-bash'
ORG_NAME = u'wrye-bash'

DEFAULT_MILESTONE_TITLE = u'Bug fixes and enhancements'
DEFAULT_AUTHORS = u'Various community members'

# OUTPUT & TEMPLATES DIRs =====================================================
OUT_DIR = u'out'

def out_path(dir_=OUT_DIR, name=u'out.txt'):
    """Returns a path joining the dir_ and name parameters. Will create the
    dirs in dir_ if not existing.

    :param dir_: a directory path
    :param name: a filename
    """
    if not os.path.exists(dir_):
        os.makedirs(dir_)
    return os.path.join(dir_, name)
