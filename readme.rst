Usage examples
--------------

Check what it would do.

::

    nbconvert_recursive.py --no-act .

Watch what it does.

::

    nbconvert_recursive.py --verbose .

See output in ``less`` pager.

::

    nbconvert_recursive.py --verbose . 2>&1 | less

Add more directories to skip.

::

    nbconvert_recursive.py --verbose . --extra-skip-dirs .dropbox.cache .insync-trash
