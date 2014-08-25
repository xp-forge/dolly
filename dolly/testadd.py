import dolly
import config
dolly.Dolly.rootdir="/home/lbentrup/dev"
p = config.Config("../config.yml")
print p.data
p.dump()
p.addRepo("git@github.com:foo/bar.git", "/home/lbentrup/dev/design/basic/foobar", "html")
print p.data
p.dump()
