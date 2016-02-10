===============
The When Wizard
===============

The **When Wizard** aims at becoming, possibly, the main interface to
**When** for those users who just want to instruct their workstations to
perform simpler tasks on a rich subset of the available conditions, or for
those system administrators who want to provide standardized sets of tasks
and events or conditions that may trigger such tasks. The **When Wizard**
is available (in *early development* stage) at its own repository_.

The **When Wizard** has been designed for extensibility: it is completely
based on plugins that are loaded by a small application core. Some plugins
are provided by default (I call them *stock plugins*), others may be
developed and easily added to the application.

.. Warning::
  The **When Wizard** is still in its early development stages, and this
  means at least that its API is still subject to changes. Such changes
  are expected to be drastically reduced before it reachs a *beta* status,
  but for now things could change abruptly, even on a convenience basis.

The main entry point for **When Wizard** extension is *plugin development*.
*Plugins* are the parts, in the application, that actually *define* items
in **When**, while the surrounding application only provides the wizard
interface and the steps that actually communicate with **When** to create
the items. Communication with **When** is made possible mainly via the
*DBus Remote API* later discussed in this manual.

There are two types of plugins that can be developed:

  * *task* plugins, and
  * *condition* plugins

even though in the latter case there are subtypes, one of which has to be
chosen when developing a *condition* plugin. *Task* plugins are probably
the ones that would gain more attention, because there are virtually
infinite tasks that can be defined to ease the user's life. But also some
types of conditions can be added as shortcuts to more complex ones:

* conditions that check *system commands*, and
* conditions that react to *user defined events*, for which the user event
  definition could be provided as an *Item Definition File*.

The following paragraphs will illustrate briefly how a plugin for the
**When Wizard** can be implemented.


.. _repository: https://github.com/almostearthling/when-wizard.git


Plugin Rationale
================

The idea behind the plugin-based structure is that it's almost impossible
to implement (or try to implement) all available reactions to all available
events, and probably also just the features that most users would like to
see are quite difficult to find and to blend with a possibly closed or
monolithic environment. Thus the plugin system: also basic functionality
is implemented as plugins in the **When Wizard**, and the system will
dynamically look for plugins both in common areas and in the user home,
making it easier to install functionality on a per-user basis.

Plugins are essentially *Python 3.x* modules with a structure, and should
obey some simple rules:

1. each plugin module *must* export a class named ``Plugin`` derived from
   either ``TaskPlugin`` or from one of the base ``...ConditionPlugin``
   classes
2. the derived class must initialize some class parameters through the
   base class constructor: many of these parameters are there for
   classification and documentation purposes only, but they end up being
   useful for a correct representation of the plugin functionality in the
   UI of the **When Wizard**
3. plugins may or may not allow for configuration in the wizard interface,
   but if they do they have to export their configuration pane through a
   well-defined interface
4. plugins should document what they do after configuration (if any) in a
   way that summarizes their purpose after configuration.

In fact all of this can lead to a plugin that does everything it has to do
just via its constructor. In many cases the plugin will sport a configuration
pane and signal functions for controls in the configuration pane, that update
the inner variables and construct the values required by the underlying task
or condition. Templates are provided for base plugins, because the plugin
structures tend to be very similar to each other, so that the coding effort
can be reduced to the bare minimum.


Reserved Attributes
===================

Instead of building a complex suite of private members and getters/setters
for base class properties, the quick approach has been chosen to directly
expose some values to the derived classes through member variables. There
are thus two types of attributes with special meanings -- which doesn't
mean that they shouldn't be accessed or changed: in some cases they *must*
be updated -- that is:

- special member variables, and
- special methods.

Most special member variables are defined at initialization time, with the
appropriate base constructor parameter:

===================== ========================================================
Variable/Parameter    Description
===================== ========================================================
category              the plugin category, must be one of the values defined
                      in ``PLUGIN_CONST`` (usually explicitly imported from
                      the ``plugin`` module): it's available only for *task*
                      plugins as a constructor parameter [#categorymod]_
basename              the base name of the plugin, should correspond to the
                      base name of the plugin file
name                  a descriptive name for the plugin, to be kept short
description           a short description of the plugin
author                the name of the plugin author
copyright             the usual copyright string, with year and so on
icon                  the name of the icon: should correspond to the base
                      name of a *PNG* file without extension either in the
                      application resource directory or in the user resource
                      directory
help_string           a sufficiently long help string: will appear in the
                      wizard box to document what the plugin does; it should
                      not exceed about four lines of text, all newlines are
                      converted to spaces.
version               a possibly sortable version string
===================== ========================================================

The values set here are available for reading withinthe plugin class in case
of need -- for example, to derive the base name of another file, such as an
icon or resource file.

There are other reserved variable names: ``unique_id``, ``module_basename``,
``module_path``, ``stock``, ``plugin_type``, ``summary_description``, and
``forward_allowed``. Most are used internally, but the last two should be
assigned in the derived class to change the behavior of the plugin:

* ``summary_description`` must be given an explanatory value that will be
  shown in the summary page of the wizard; it can be modified while the
  plugin is being configured and can contain values of the configuration
  parameters
* ``forward_allowed`` should be set to ``False`` in the derived plugin
  constructor if the default values for its parameters (that is, the ones
  that will be first shown in the configuration pane) *must* be modified
  before the wizard can step forward; if it's set to ``False``, then the
  ``allow_forward()`` method shown below must be used to enable the *Next*
  button.

All plugins have these methods:

===================== ========================================================
Method                Description
===================== ========================================================
get_dialog(name)      returns a `dialog builder`_ object from a file that has
                      the base name (without extension: supported extensions
                      are ``.ui`` and ``.glade``) as the provided parameter
get_image(name)       returns a `pixbuf` loaded from a file whose base name
                      is the provided parameter; icons are looked for in two
                      paths: the user resource path and the application
                      resource path, so that a non-stock plugin can also use
                      one of the icons that come with the application
get_script(filename)  returns the full path to an executable script if it is
                      needed by the plugin either to execute an action or to
                      test a condition; the filename should be the base name
                      only, including any extension (like ``.py`` or ``.sh``)
allow_forward()       if called without arguments (or with ``True`` as
                      argument) it causes the wizard button to become
                      *sensitive*: it has to be called when the configuration
                      pane controls contain acceptable data; if a ``False``
                      parameter is provided, the wizard button will become
                      *not sensitive*
get_pane()            if the plugin has a configuration pane, this method
                      *must* be overridden and return a reference to the
                      outmost container object in the plugin pane dialog
                      structure.
===================== ========================================================

There are also other reserved method names common to all pugins: ``to_dict``,
``from_dict``, ``to_item_dict``, ``to_itemdef_dict``, ``to_itemdef``,
``desc_string_gui``, ``desc_string_console``, ``data_store``,
``data_retrieve``, ``set_forward_button``, and ``get_config``. These names
should not be overridden in plugin implementations as overriding them would
cause the plugin not to work properly.


.. _`dialog builder`: https://python-gtk-3-tutorial.readthedocs.org/en/latest/builder.html


Task Plugins
============

Task plugins should just provide a *command line* that will be run whenever
the associated condition occurs. The easiest case is when the command is
fixed and no configuration is needed: in such a case the constructor will
define the command and no other code is needed. For example, the command to
lock a session is

::

  $ dm-tool lock

with no configurable options. This means that a plugin whose task is to lock
the running session will only configure the ``command_line`` member variable
of the task plugin to be ``dm-tool lock``.

The variables that can be set in a task plugin to modify its behavior are the
following:

================= ============================================================
Variable          Description
================= ============================================================
command_line      the command that will be executed by the task in its
                  entirety, including parameters: it will be executed in a
                  shell, so it can also be the path to a script
process_wait      determine whether or not the calling process should wait
                  for the called process to end; for simple tasks it is
                  safe to skip this and let the process be left alone as
                  soon as it is started
================= ============================================================

In case a task plugin should be configured, the ``get_pane()`` method must be
overridden to return a reference to the outmost container of the configuration
pane, and dialog signal handling functions must be defined to retrieve
configuration values from the pane just as if it were a standard *Gtk* dialog
box.

Task plugins also give the possibility to set one and only one of the
following variables:

=============== ==============================================================
Variable        Description
=============== ==============================================================
success_status  if the status code of the called process has to be checked
                for a specific success value; must be an integer and
                defaults to ``0``
failure_status  if the status code of the called process has to be checked
                for a specific failure value; must be an integer
success_stdout  a string that, if corresponding to process output (written
                to *stdout*), will let the process execution be considered
                a success; modifiers specified below can change the way the
                correspondance is checked
failure_stdout  a string that, if corresponding to process output (written
                to *stdout*), will let the process execution be considered
                a failure; same as above for modifiers
success_stderr  string that, if corresponding to process output (written
                to *stderr*), will let the process execution be considered
                a success; same as above for modifiers
failure_stderr  a string that, if corresponding to process output (written
                to *stderr*), will let the process execution be considered
                a failure; same as above for modifiers
=============== ==============================================================

and these are the modifiers for string *stdout/stderr* variables:

===================== ========================================================
Variable              Description
===================== ========================================================
match_exact_output    if the specified string should match from start to end,
                      if ``False`` the correspondance will be found when the
                      given string is contained in the output
match_case_sensitive  if true the comparison is case sensitive
match_regexp          if true the given string is considered a regular
                      expression and matched against the process output
===================== ========================================================

These attributes are all booleans, and default to ``False``: output will be
searched for a substring with no distinction between uppercase and lowercase.
Values for the modifier variables can be set independently on all of them:
for example if ``match_exact_output`` is set to ``True`` and ``match_regexp``
too, the provided regular expression will be checked at the beginning of the
process output, if ``match_exact_output`` is ``False`` **When** will just try
to find a match for the regular expression in the output.

The base class for this type of plugin is ``TaskPlugin``: at the beginning
of a plugin there must always be the following statement

.. code-block:: python

  from plugin import TaskPlugin, PLUGIN_CONST

in order to derive the ``Plugin`` class. The above mentioned ``category``
base constructor parameter can be given one of the following values:

=================================== ==========================================
Constant                            Related plugins
=================================== ==========================================
PLUGIN_CONST.CATEGORY_TASK_APPS     For plugins that concern applications,
                                    such as starting or killing a program or
                                    system utility
PLUGIN_CONST.CATEGORY_TASK_SETTINGS When the plugin manages session, desktop
                                    or system settings
PLUGIN_CONST.CATEGORY_TASK_POWER    For power-management related plugins
PLUGIN_CONST.CATEGORY_TASK_SESSION  For session management related plugins,
                                    like session lock, unlock or logout
PLUGIN_CONST.CATEGORY_TASK_FILEOPS  This has to be used for plugins that
                                    perform file operation, such as backups
                                    or synchronizations
PLUGIN_CONST.CATEGORY_TASK_MISC     All other task plugins belong here
=================================== ==========================================

These values should be assigned carefully, because the user will be able to
choose a plugin only after category has been selected.


Condition Plugins
=================

There are several types of condition plugins: for each type the appropriate
base class must be used. In the same way as for task plugins, the base class
be imported in the plugin code:

.. code-block:: python

  from plugin import <SpecificConditionPlugin>, PLUGIN_CONST

where ``<SpecificConditionPlugin>`` must be replaced with one of the names
specified below. The plugin category is determined by the condition plugin
type, but in case the developed plugin belongs to a different category, its
value can be assigned one of the following constants:

================================= ============================================
Constant                          Related plugins
================================= ============================================
PLUGIN_CONST.CATEGORY_COND_TIME   Category for plugins that define conditions
                                  concerning time: *time*, *idle time*, and
                                  *interval* based conditions normally belong
                                  to this category
PLUGIN_CONST.CATEGORY_COND_EVENT  Category for plugins that define conditions
                                  related to stock and user defined *events*
PLUGIN_CONST.CATEGORY_COND_MISC   All other condition plugins belong here
================================= ============================================

The ``category`` member variable can be reassigned *after* the base class
constructor has been called -- otherwise the new category is overwritten.

There are some *flags* (in the form of attributes, as usual) that can be set
to either ``True`` or ``False`` to change how the generated condition check
will behave:

================= ============================================================
Variable          Description
================= ============================================================
sequential        if there is a task list instead of a single associated task
                  the tasks in the list are run sequentially; since the
                  application only provides conditions associated with single
                  tasks this flag can be left alone; set to ``True`` by
                  default
repeat            if ``True`` checks will persist after first successful one
suspended         if ``True`` then checks for the associated condition are
                  suspended on condition registration
break_on_failure  when a sequence of tasks is given, break after the first
                  failed task; normally it is ignored, and defaults to
                  ``False``
break_on_success  when a sequence of tasks is given, break after the first
                  successful task; normally it is ignored, and defaults to
                  ``False``
================= ============================================================

Other attributes, methods and other member data may be present in subclasses
that can be derived from, as specifically described below.


Interval Based Condition Plugins
--------------------------------

Such plugins must provide the length of an interval in minutes, in the
``interval`` member variable. A simple plugin of this kind is already
provided by the application and derivatives are unlikely to be actually
useful.

The base class for this type of plugin is ``IntervalConditionPlugin``.


Time Based Condition Plugins
----------------------------

Plugins of this type must define a time specification dictionary in the
``timespec`` member variable: the dictionary values are integers, with the
following keys (as strings):

* ``'year'``
* ``'month'``
* ``'day'``
* ``'hour'``
* ``'minute'``
* ``'weekday'``

The ``'weekday'`` key, if used, allows for week-based repetition. A value
of ``0`` is for monday, ``6`` is for sunday. It should not be used in
conjunction with other date specifications. Values that must not be checked
can just be skipped: for a condition that must occur at quarter past any
hour of the day, just

.. code-block:: python

  self.timespec['minute'] = 15

should be set in the plugin. Instead of providing a single plugin of this
type with all possible settings, several plugins with more specific scope
can be a better option to give the users an easier way to choose what kind
of time based condition they need.

The base class for this type of plugin is ``TimeConditionPlugin``.


Idle Time Based Condition Plugins
---------------------------------

In this type of plugin the ``idlemins`` member variable must contain the
time in minutes that the session has to be idle before the condition occurs;
since a simple plugin of this kind is already provided, this one is unlikely
to be derived.

The base class for this type of plugin is ``IdleConditionPlugin``.


File Change Based Condition Plugins
-----------------------------------

In these a path containing a file or directory to be watched must be provided
using the ``watched_path`` string member variable. Stock plugins, one for
files and another one for directories, are already available.

The base class for this type of plugin is ``FileChangeConditionPlugin``.


Stock Event Based Condition Plugins
-----------------------------------

These plugins provide the counterpart of the *Event Based Conditions* in the
**When** applet, and only occur when stock events occur. They must hold the
event name in the ``event`` member variable, and are unlikely to need any
form of configuration. However plugins for stock events are provided by the
application, the only exception being possibly command line driven events,
which are virtually useless in the **When Wizard** context.

The base class for this type of plugin is ``EventConditionPlugin``.


User-Defined Event Based Condition Plugins
------------------------------------------

Plugins of this kind must store the name of the user-defined event (as known
by **When**, thus the name that has been possibly given to the event in an
*Item Definition File*) in the ``event_name`` member variable. These can be
very useful to create condition that occur on events that are not handled by
**When** by default, and the possibilities are virtually endless.

Because the corresponding conditions occur when the related *DBus* signal is
fired, in most cases the related plugins will need no configuration pane.

The base class for this type of plugin is ``UserEventConditionPlugin``.


Command Based Condition Plugins
-------------------------------

Command based conditions are probably the ones that will benefit most from
the implementation of specific plugins: almost every check can be done
using system commands, possibly combined into scripts, and many types of
event can be discovered or triggered in this way.

Such conditions are possibly where **When** can show the highest flexibility,
but are also the ones that require a certain knowledge of Linux, of the
shell and the system commands, and that might require some programming
skills. The ability to include scripts with the plugin and the possibility
to modify the command line using data gathered through the pane-based
configuration gives the possibility to check for whatever actual status of
the system -- from the availability of files or devices to the connection
status or the existence of resources online, just to mention a few.

Plugins of this type must store the actual command line in the
``command_line`` member variable, and depending on the command result the
related event will either occur or not.

Just like in `Task Plugins`_ there are attributes to check command outcome:
since there is no concept of success or failure in conditions, but just
either occurrence or not, the attributes only specify what to expect.

=============== ==============================================================
Variable        Description
=============== ==============================================================
expected_status the status that the called process should return to consider
                the underlying condition to occur, integer defaulting to ``0``
expected_stdout string to find a correspondence for in the *standard output*
expected_stderr string to find a correspondence for in the *standard error*
=============== ==============================================================

Here too modifiers are available, as for *Task Plugins*, and have the same
identifiers and specifications:

===================== ========================================================
Variable              Description
===================== ========================================================
match_exact_output    if the specified string should match from start to end,
                      if ``False`` the correspondance will be found when the
                      given string is contained in the output
match_case_sensitive  if true the comparison is case sensitive
match_regexp          if true the given string is considered a regular
                      expression and matched against the process output
===================== ========================================================

The base class for this type of plugin is ``CommandConditionPlugin``.


.. [#categorymod] For condition plugins the category is automatically set
  depending on the type of condition plugin the actual plugin is derived
  from. However it can be changed after invoking the base class constructor
  if the automatic setting does not fit the nature of the plugin.
