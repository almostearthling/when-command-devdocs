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

The applet is in fact a small utility, and I thought it would have even
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


How Can I Help?
===============

There are several ways to help. Even though **When** has been developed for
a while now and has a quite thorough `Test Suite`_, the devil can still
figure out a way to stay around in the details. Such details can be of
several kinds: be it bugs, missing features or whatever else, they have to
be addressed. So, here is what can be done to help development of **When**.

Review the code
---------------

A lot can be done by reviewing the code. The single Python file is quite big
now, and although I tried to keep it as tidy as possible, it still might
contain places where it's hard to read. For example, in a quite recent beta
tag (*v0.9.7-beta.3* to be exact) I finally removed a completely useless
operation that was dangling there probably from the very beginning. Issues
with the code may include:

* useless or redundant parts
* things that could be done in a more optimized way -- as long as it does
  not introduce inelegance or obscurity
* excessive logging
* incorrect language in output, UI and comments
* inconsistent identifiers (variable and function names, mostly), or even
  names that are just inexplicative.

Interventions in this field can be done either using the *issue* mechanism
or just by telling me otherwise what's supposedly wrong with the code and
suggesting possible amendments.

Review the Documentation
------------------------

This is important. At this point it should be clear that I'm not a native
English speaker or writer. And, even worse, I don't have anyone at hand who
can proofread these documents. So, if there is any volunteer out there who
would like to help in this field, feel free to throw an *issue* in the
related repository:

* `User Documentation`_
* `Contribution Guide`_

Also, within the `User Documentation`_, a part that can be improved is the
`Tutorial`_, where probably more complete examples could be provided. If you
use **When** and have an example that is particularly useful, feel free to
submit it.

Other Linux Distributions
-------------------------

In my opinion **When** is now ready to better support other Linux distros
that use *GLib* and/or *Gnome*. The *fallback* mechanism used to implement
stock events should allow easy creation of fallback entries where DBus
functionality specific to *Ubuntu* is not available. Packaging_ too is a
quite important in supporting other distributions.

Improve the Test Suite
----------------------

I tried to make the `Test Suite`_ as thorough as possible, and in fact it
covers almost all features (with the exception of most UI/UX parts, because
they are quite hard to test). Obviously there should still be something left
out. The completeness of tests gives more chances that the final product is
actually working, and makes the task of porting **When** to other Linux
distributions much easier and obviously quicker. Improvements are of course
possible by adding more tests (as long as they are not redundant), but also
by making the existing components of the suite itself easier to read and to
modify. Another aspect where the `Test Suite`_ can be improved, is the
compatibility with `continuous integration`_ (CI) tools: I'd like to have
**When** tested in `Travis CI`_ some day, but for the moment I am not able
to figure out how to get there.

Localization
------------

**When** has support for localization_, described in this guide. Also, this
guide provides some hints on how to localize the applet in your language.
Feel free to provide a translation if you want, you will be credited for
the contribution.

Packaging
---------

Packaging is another place where things could be better. Firstly, the
*Ubuntu* package (LSB version) installs and blends acceptably with the
distribution, but there are still some rough edges to smooth off, such as
the translations that should be separated from the rest of the program.
Also, packages specific to other distributions that might be supported
should be created.

Add-ons
-------

With release *v0.9.7-beta.3* **When** has gained an almost full DBus API,
documented later in this guide, which can be used to interact with a running
instance of the applet. Using this interface and its provided methods, the
applet can be configured using an external application. I am on the way to
providing a more streamlined interface (I'm calling it the **When Wizard**)
for users that would like the complexity of the *"raw"* applet hidden, and
a wizard-like tool with a library of *conditions* and *tasks* ready for
general use. [#wizard]_


.. _`Test Suite`: https://github.com/almostearthling/when-command-testsuite
.. _`User Documentation`: https://github.com/almostearthling/when-command-docs
.. _`Contribution Guide`: https://github.com/almostearthling/when-command-devdocs
.. _`tutorial`: http://when-documentation.readthedocs.org/en/latest/tutorial.html
.. _`continuous integration`: https://en.wikipedia.org/wiki/Continuous_integration
.. _`Travis CI`: https://travis-ci.org/


.. [#reqs] In fact the other packages that could possibly require installation
  are the ones mentioned in the chapter devoted to the applet install process.
  No *-dev* packages should be needed because **When** is entirely developed
  in the Python language.

.. [#wizard] As soon as I publish an early release of this application, there
  will also be a dedicated section for it in this developer guide.
