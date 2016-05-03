===============
DBus Remote API
===============

Starting with version *v0.9.7-beta.3* (not corresponding to a packaged release
though) **When** has gained a *remote API* through DBus. This API can be used
to control various aspects of a running instance of **When**, so that it can
even be almost completely managed by an external application. Operations
available through the remote API cover:

* managing all types of items: *tasks*, *conditions* and *signal handlers*
* managing the configuration and configuration file
* pausing or resetting a running instance
* retrieving current history

and more. This interface has been created to allow development of a companion
application, the upcoming **When Wizard**, that will provide a different and
easier way to manage **When** letting it only perform as a mere engine.

**When** exposes methods that are somehow *reserved* for itself (mainly the
ones that allow communication between the command line utility and a running
applet instance), *and* also methods that are available for external control.
This section only briefly documents the former ones, while trying to be more
extensive with the latter type.


Interface
=========

Details on how to estabilish DBus a connection to the **When** applet follow:

=============== =============================================================
Item            Value
=============== =============================================================
Bus             *session*
Application ID  ``it.jks.WhenCommand``
Unique Bus ID   ``it.jks.WhenCommand.BusService``
Object Path     ``/it/jks/WhenCommand/BusService``
Interface       ``it.jks.WhenCommand.BusService``
=============== =============================================================

These values can be used to build a *proxy* to the **When** interface, see
the DBus documentation for more details. Specifically, to build a proxy in
*Python* the following model can be used:

::

  import dbus

  bus = dbus.SessionBus()
  proxy = bus.get_object('it.jks.WhenCommand.BusService',
                         '/it/jks/WhenCommand/BusService')

It will give access to the whole API in the form ``proxy.call(p1[, p2 ...])``
where ``call`` is the name of an API method (see below) and ``pN`` are the
parameters expected by the method.


General Use Methods
===================

The following methods have been designed aiming at interoperability, thus
they are useful for the purposes explained above.

=================================== ==========================================
Method                              Description
=================================== ==========================================
``AddItemByDefinition(dic, save)``  add an item to the collection of items
                                    managed by **When**, and optionally save
                                    the collection where the item belongs.
                                    The item must be provided in dictionary
                                    form, as specified below, in the ``dic``
                                    parameter, while the ``save`` argument
                                    is a boolean indicating whether or not to
                                    save the collection; returns *True* on
                                    success, *False* ortherwise [#dic]_
``AddItemsBatch(item_data)``        add multiple items using a string in the
                                    *item definition file* format (see the
                                    `user guide`_ for detailed information);
                                    the argument should follow the format
                                    exactly, with newlines, indents and so on;
                                    returns *True* on success, *False*
                                    ortherwise
``GetConfig(section, entry)``       return a value (enclosed in a *variant*)
                                    from the running configuration, which in
                                    turn most likely reflects the same value
                                    in the configuration file; ``section``
                                    and ``entry`` are strings [#variant]_
``GetHistoryEntries()``             return the list of entries in thehistory
                                    of the running instance: the entries are
                                    returned as a list of strings,
                                    corresponding each to a line of an
                                    exported history file -- except for
                                    headers -- that is a semicolon separated
                                    list of values
``GetItemDefinition(item_spec)``    given an *item specification* [#itemspec]_
                                    as argument, return the definition of the
                                    corresponding item as a mapping
                                    (dictionary) if it exists [#dic]_
``GetItemNames(item_type)``         return a list of item names possibly
                                    corresponding to the specified type
                                    of item if the ``item_type`` parameter
                                    is one of ``'tasks'``, ``'conditions'``
                                    and ``'sighandlers'`` (or an abbreviation
                                    thereof), or all items if the empty string
                                    is passed
``IsSuspendedCondition(cond_name)`` tell whether or not the condition whose
                                    name is provided as argument is suspended
``Pause(pause)``                    set the paused state to the one provided
                                    in the *boolean* ``pause`` argument:
                                    paused if *True*, resumed if *False*
``Paused()``                        return the current paused state as a
                                    self-explanatory *boolean* value
``ReloadConfig()``                  reconfigure the applet from static data
``RemoveItem(item_spec)``           given an *item specification* [#itemspec]_
                                    remove the corresponding item; returns
                                    *True* on success, *False* ortherwise
``Reset(clear_history)``            reset the applet and reload data, similar
                                    to a *restart* but without running startup
                                    and shutdown actions; if the
                                    ``clear_history`` parameter is set to
                                    *True* also clear the current task history
``SaveItems(item_type)``            save all items of the type provided in
                                    ``item_type`` (see ``GetItemNames`` above
                                    on how to specify it), all items are saved
                                    when providing the empty string
``SetConfig(sec, ent, v, reload)``  set the configuration entry ``ent`` at
                                    section ``sec`` in the running applet
                                    to the value specified in ``v`` (which
                                    must be provided as a *variant*); if
                                    the *boolean* argument ``reload`` is set
                                    to *True* the configuration is reloaded
                                    after the operation; returns *True* on
                                    success and *False* on failure
``SuspendCondition(cond_name, s)``  if ``s`` is *True* the condition is
                                    suspended, if *False* it is resumed
=================================== ==========================================

*Item definition* dictionaries returned by ``GetItemDefinition`` and handled
by ``AddItemByDefinition`` are implemented using strings as keys and variants
as values.

.. _`user guide`: http://when-documentation.readthedocs.io/


Reserved Methods
================

Methods that should be avoided generally are: ``ExportHistory`` that exports
history entries to a file given its name, ``KillInstance`` and
``QuitInstance`` (especiatlly the former) that causes the applet to exit,
``RunCLIBasedCondition`` that is only used to force a *command-line based*
condition to occur and ``ShowDialog`` to fire up a dialog box. These methods
are only used with ``when-command`` as a controlling utility, and are pretty
useless in external applications.


.. [#dic] the DBus documentation explains how to access *DBus dictionaries*;
  in this particular case the keys are *strings* and values must be enclosed
  in *variant* objects.

.. [#variant] sometimes **When** expects data to be enclosed in a *variant*
  container: there are several methods to achieve this, including the use
  of the ``GLib.Variant`` (``GLib::Variant``) constructor.

.. [#itemspec] a string consisting of the tipe of item (or an abbreviation
  thereof) in `tasks`, `conditions`, and `sighandlers`, following by a
  colon and the unique name of the item itself. For example, if there is a
  task named ``SomeTask``, then ``task:SomeTask`` is a correct item
  specification (where *task* is actually an abbreviation of the more
  general *tasks*).
