## Debugging: Reload a package
The `importlib.reload` module allows you to reload a package without closing and restarting a python session.
When I am developing in a notebook that uses imported functions from another module I have written, I sometimes need to make changes to the imported 
module. But simply rerunning the cell that imported the module would not reload the module with the changes I made to that module. I used to think I had 
to rerun the entire script I was working on to included the edits to that module, but you can actually do a hard reload of a package with the importlib.
reload module.
Note that reloading doesn't appear to work for single functions from a package. For example, if you have a function called do_this in a package called my
_pkg , then this will not work:

```python
# DOES NOT WORK!
from my_pkg import do_this
reload(do_this)

# THIS DOES WORK :)
import my_pkg as pkg
reload(pkg)
pkg.do_this()

```
