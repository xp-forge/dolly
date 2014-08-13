# Dolly

```

     _     ,--.      |    |
  _-(_)-   |   |,---.|    |    ,   .
`(___)     |   ||   ||    |    |   |
 // \\     `--' `---'`---'`---'`---|
                               `---'
```

Dolly manages multiple Git and Svn repos.

## Config

The config file can be specified with the `-c` parameter.
If no file is specified it looks in `~/.dolly.yml` and `/etc/dolly.yml`
(in that order)

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

In the example the repo '2048' will be placed in `$ROOT_DIR/games/html/js`