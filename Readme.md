This is the Wrye Bash meta repository, containing Bethesda forums thread
starter posts (Oblivion and Skyrim), nexus description pages, release changelogs
in various formats and some scripts to generate these as well as second posts.
The scripts depend on the [PyGithub][1] module to interface with github -
see link for installation.

##### Content:

__Do not edit the content directly__.
Instead run the scripts (see below for command line usage and important info
but keep in mind that you can also run them by double click and they will
prompt for required parameters - do install Python launcher for windows).
If you want to edit the form of the posts edit the relevant template. The posts
are versioned here so one can easily diff the scripts' output but are not meant
to be edited directly.</br>
The content is distributed in the following directories:

- __scripts__: the scripts for generating forum posts, changelogs  etc by
reading the wrye-bash/wrye-bash repository data. Depend on [PyGithub][1].
Subdirectories:
  * _scripts/templates_: contains templates for the scripts to operate upon
(WIP)
  * _scripts/out (not versioned)_: used for outputting the posts that either
belong to another repo (eg Version History.html) or change too frequently to be
versioned (eg the second posts in the Bethesda forums)
  * _scripts/helpers_: helpers for the scripts, including a github wrapper for
getting issues (features caching), formatting (html, bbcode and markdown) and
parsing the ini file.
- __ChangeLogs__: contains changelogs for the last few releases in the various
text formats we use (bbcode, html, markdown).
- __FirstPosts__: forum thread starters, currently Oblivion and Skyrim.
- __NexusDescriptionPages__ : for Oblivion and Skyrim.

##### Using the scripts

All scripts use the [argparse][2] module to parse command line arguments - so
use `-h` to display usage. In short the scripts fall into two categories -
online and offline. To run the offline ones you need to generate the changelogs
for the latest release.

- Generate the changelogs - the milestone  is the _latest_ release:

        generate_changelog.py -m 304.4 -t "Move to git" -o

  where the `-o` flag prevents overwrite of existing changelogs for the specified
milestone. __NB__: by default the scripts _override their previous output if any_.
The script will spit out an `issues.###.txt` file and will allow you to edit
it (`###` is the milestone number from the `-m` argument). Then it will generate
the changelogs in markdown, bbcode and html formats
based on this txt. If you pass the `--offline` flag the script will
directly use the `issues.###.txt` file (will not redownload the issues from
github). So just run the script once to generate the txt and then edit the txt
at your heart's content and regenerate the formatted changelogs running
generate_changelog.py with the offline flag.

Once you have the changelogs for the latest release you can run the rest of the
scripts.

- Generate the first posts:

        generate_first_posts.py -m 304.4 -e "C:\\__\\Notepad++\\notepad++.exe"

  They will use the changelogs you generated and the values for current and
previous threads as specified in the `scripts/values.ini` file. So if you want
to generate the posts because of a new release then _generate the changelogs
first_ - if you want to generate the posts because of thread change you must
first update `values.ini` with proper thread numbers. An editor will
pop up where you can manually tweak them (mind the thread numbers and dates).
The default editor is `C:\\Program Files\\Notepad++\\notepad++.exe`. Specify
`no_editor` to skip this (not recommended).

- Generate the version history html:

        generate_version_history.py -m 304.4  -e "C:\\__\\Notepad++\\notepad++.exe"

 (304.4 stands for the latest release). The script should let you edit the file
then will copy it to the wrye-bash and github.io repos (provided they are
cloned in the same directory as meta).

- Generate the nexus description pages (Oblivion and Skyrim):

        generate_nexus_description.py -m 304.4 -e "C:\\__\\Notepad++\\notepad++.exe"

 (304.4 stands for the latest release). The script will let you edit the files,
you should only need to do this when a new release (including beta ones) is out
or if you want to change the description (by editing
`scripts/templates/generate_nexus_description_lines.txt`).

##### Second posts

The second posts also need access to github.
To generate the second posts just use `generate_second_posts.py -m 305` where
now the milestone corresponds to the ___next___ release. The posts will be
dumped into `scripts/out/SecondPosts`.<br/>

[1]: https://github.com/jacquev6/PyGithub
[2]: https://docs.python.org/2/library/argparse.html#module-argparse
