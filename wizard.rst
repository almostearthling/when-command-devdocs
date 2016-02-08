===============
The When Wizard
===============

The **When Wizard** aims at becoming, possibly, the main interface to
**When** for those users who just want to instruct their workstations to
perform simpler tasks on a rich subset of the available conditions, or for
those system administrators who want to provide standardized sets of tasks
and events or conditions that may trigger such tasks.

The **When Wizard** has been designed for extensibility: it is completely
based on plugins that are loaded by a small application core. Some plugins
are provided by default (i call them *stock plugins*), others may be
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





.. [#categorymod] For condition plugins the category is automatically set
  depending on the type of condition plugin the actual plugin is derived
  from. However it can be changed after invoking the base class constructor
  if the automatic setting does not fit the nature of the plugin.
