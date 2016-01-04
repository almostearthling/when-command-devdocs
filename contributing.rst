============
Contributing
============

**When** is open source software, this means that contributions are welcome.
To contribute with code, please consider following the minimal recommendations
that usually apply to the software published on GitHub:

1. Fork the `When repository`_ and pull it to your working directory
2. Create a branch for the new feature or fix: ``git checkout -b new-branch``
3. Edit the code and commit: ``git commit -am "Add this feature to When"``
4. Push your changes to the new branch: ``git push origin new-branch``
5. Compare and submit a `Pull Request`_.

A more general discussion about contribution can be found here_. Otherwise,
just submit an issue to notify a bug, a mistake or something that could just
have been implemented better. Just consider that the applet is intended to be
and remain small in terms of code and features, so that it can stay in the
background of an user session without disturbing it too much.

.. _`When Repository`: https://github.com/almostearthling/when-command
.. _`Pull Request`: https://github.com/almostearthling/when-command/compare
.. _here: https://help.github.com/articles/using-pull-requests


Some Notes about the Code
=========================

The applet is in fact a small utility, and I thought it also would have even
less features. It grew a little just because some of the features could be
added almost for free, so the "*Why Not?*" part of the development process
has been quite consistent for a while. The first usable version of the applet
has been developed in about two weeks, most of which spent learning how to use
*PyGObject* and friends, and not on a full time basis: by the 5th day I had to
freeze the features and focus on the ones I wrote down. So, being small and
mostly not reusable, the single-source option seemed the most obvious, also
to keep the package as self-contained as possible. However, the way the applet
starts and defines its own system-wide and user directories allows the
development of modules that can be imported without cluttering and polluting
the system: the ``APP_DATA_FOLDER`` variable defines a dedicated directory
for the application where modules can be installed, and normally it points to
``<install-base>/when-command/share`` or ``/usr/[local/]share/when-command``
or something similar and well identifiable anyway.

The code tries to follow the usual guidelines for Python 3.x, and takes
inspiration from other Gnome applets that sit in the indicator tray. I tried
to reduce the comments to the very least, and let the code speak for itself.
Some of the conventions here are the following:

* system wide constants are spelled in all uppercase (as usual in *C/C++*)
* variables tend to be all lowercase, both globals and locals
* class names start with an uppercase letter and are in camelcase
* global instances of classes are lowercase, like simple variables
* private members start, as usual, with an underscore
* function names are all lowercase with underscores
* transitional (or debug) functions start with underscores
* the core classes implement their own loggers, borrowing from the global one
* user interaction strings (and log messages) use double quotes
* program internal strings use single quotes
* statements tend to be split in lines of at most 80 characters, apart from
  log messages
* log messages mostly sport a prefix to determine what part generated them
* log messages containing the ``NTBS`` strings are *never to be seen*.

All user interaction strings (except log messages) are surrounded by the
usual ``_(...)`` formula used in software that implements the ``gettext``
functions: this allows to translate **When** without intervention on the code
itself, in the usual fashion for Linux applications.


Dependencies
============

Being an applet oriented mostly towards users of recent Ubuntu editions, it
is developed in *Python 3.x* and uses the latest supported edition of
*PyGObject* at the time. It shouldn't rely on other packages than
``python3-gi`` and ``python3-pyinotify`` on the Python side. [#reqs]_ The
*Glade* user interface designer is almost mandatory to edit the dialog boxes.

To implement the "*Idle Session*" based condition (i.e. the one that lets a
task run when the session has been idle for a while), however, the external
``xprintidle`` command may be used that is not installed by default on Ubuntu.
As of version *0.9.6-beta.1* it is no more strictly necessary, however the
dependency is kept (also in packages) because it could be used as a fallback
method for detecting idle time when ``libXss`` cannot be linked, and because
it causes an implicit dependency from ``libXss`` itself. Normally if ``libXss``
is installed and **When** is run from a source code based installation, the
installation of ``xprintidle`` can be safely skipped.


.. [#reqs] In fact the other packages that could possibly require installation
  are the ones mentioned in the chapter devoted to the applet install process.
  No *-dev* packages should be needed because **When** is entirely developed
  in the Python language.
