# Dolly

[![Build Status](https://travis-ci.org/xp-forge/dolly.svg?branch=master)](https://travis-ci.org/xp-forge/dolly)

```

     _     ,--.      |    |
  _-(_)-   |   |,---.|    |    ,   .
`(___)     |   ||   ||    |    |   |
 // \\     `--' `---'`---'`---'`---|
                               `---'
```

Dolly manages multiple Git and SVN repos.

## Usage
```
dolly [-h] [-v] [-r ROOTDIR] [-c CONFIG] command [project]
```

Dolly can be run in the command line with `dolly` or `dly`.

It takes a command argument and an optional project argument.
Valid commands are:

* `help` to print the help menu
* `list` to list the repositories of the specified project (and all included projects)
* `status` to get uncommitted changes and unpushed commits
* `update` to pull and clone
* `install` to clone repositories that aren't yet on disk
* `list-dirs` to print all local repo paths (useful in scripts)

The action will run for every repository in the specified projects tree and all included projects.

If no project parameter is given Dolly will look for a `default` project.


## Configuration

The config file can be specified with the `-c` parameter.
If no file is specified it looks in `~/.dolly.yml` and `/etc/dolly/dolly.yml`
(in that order).

### Example
```
games:
  description: "HTML5 / JS games"
  post_update: "echo $(date) > /tmp/games"
  tree:
    games/html/js:
      - '2048': https://github.com/gabrielecirulli/2048.git
design-essentials:
  description: "GitHub featured"
  tree:
    design/html/js:
      - flint: https://github.com/pengwynn/flint
      - normalize: https://github.com/necolas/normalize.css
html:
  description: "Stuff"
  tree:
    design/basic:
      - moderinzr: https://github.com/Modernizr/Modernizr.git

gameshtml:
  description: "TL;DW"
  includes:
    - html
    - games

default:
  description: "TL;DW"
  includes:
    - design-essentials
    - gameshtml
  tree:
    foo/bar:
      - testproj: git@git.1and1.org:lbentrup/automation-tools.git
    bar/foo:
      - clumsybird: https://github.com/ellisonleao/clumsy-bird.git
```

### Extended repository syntax
At the moment, the properties "tag" and "branch" are only supported by git.
```
...
tree;
  - name: 'modernizer'
    repository: https://github.com/Modernizr/Modernizr.git
    tag: v2.8.1
    post_update: echo done
  - name: 'modernizerback'
    repository: https://github.com/Modernizr/Modernizr.git
    branch: back
    post_update: echo done
...
```

In the example the repo '2048' will be placed in `$ROOT_DIR/games/html/js`.

The `default` project also includes the `design-essentials` and `html` projects. So when the `default` project is processed, all of the repos in this config file will be processed.

If a project is included multiple times, it is only processed once.

## Installation

Dolly can be installed using pip with

```bash
pip install dolly    # Add --upgrade to update dolly
```

This will also install the following dependencies:
* argparse
* pyyaml

To install from this git repo:

```
git clone https://github.com/xp-forge/dolly.git
cd dolly
sudo python setup.py install
```
