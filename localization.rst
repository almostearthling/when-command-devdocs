============
Localization
============

Starting with version *0.9.1-beta.2* **When** supports the standard
localization paradigm for Linux software, via ``gettext`` and its companion
functions. This means that all translation work can be done with the usual
tools available on Linux, that is:

* ``xgettext`` (for the Python source) and ``intltool-extract`` (for the
  *Glade* UI files)
* ``msginit``, ``msgmerge`` and ``msgfmt``

This should allow for easier translation of the software. In fact I provide
the Italian localization (it's the easiest one for me): help is obviously
welcome and really appreciated for other ones.

I can provide some simple instructions for volunteers that would like to
help translate **When** in other languages: I've already seen some activity
in this sense, and very quickly after the first public announcement. I'm
really glad of it, because it helps **When** become more complete and usable.

Think of the following instructions more as a *recipe* than as an official
method to carry the translation tasks.


Template Generation
===================

.. Note::
  Normally, to translate the applet, a translator only needs access to the
  most recent *message template* (which is ``po/messages.pot``); however these
  instructions also try to show how to generate such template in case some
  text in the source has changed, for example while fixing a bug.

Basically the necessary tools are:

* ``intltool-extract`` to retrieve text from the UI files
* ``xgettext`` to extract text from the main applet source.

When in the source tree base, the following commands can be used to generate
the template without cluttering the rest of the source tree:

::

  $ mkdir .temp
  $ for x in share/when-command/*.glade ; do
  >   intltool-extract --type=gettext/glade $x
  >   mv -f $x.h .temp
  > done
  $ xgettext -k_ -kN_ -o po/messages.pot -D share/when-command -D .temp -f po/translate.list

After template generation, which is stored in ``po/messages.pot``, the
``.temp`` directory can be safely deleted. If ``po/messages.pot`` already
exists and is up to date, this step can be skipped.


Create and Update Translations
==============================

To create a translation, one should be in a localized environment:

::

  $ cd po
  $ export LANG=it_IT
  $ msginit --locale=it_IT --input=po/messages.pot --output=po/it.po

where ``it_IT`` is used as an example and should be changed for other locales.
For all ``po/*.po`` files (in this case ``it.po`` is created), the following
command can be used to create an updated file without losing existing work:

::

  $ msgmerge -U po/it.po po/messages.pot

where ``it.po`` should be changed according to locale to translate. The
generated or updated ``.po`` file has to be modified by adding or updating the
translation, and there are at least two options for it:

* use a standard text editor (the applet source and string set is small enough
  to allow it)
* use a dedicated tool like poedit_.

After editing the *portable object*, it must be compiled and moved to the
appropriate directory for proper installation, as shown below.

.. _poedit: https://poedit.net/


Create the Object File
======================

When the ``.po`` file has been edited appropriately, the following commands
create a compiled localization file in a subtree of ``share/locale`` that is
ready for packaging and distribution:

::

  $ mkdir -p share/locale/it/LC_MESSAGES
  $ msgfmt po/it.po -o share/locale/it/LC_MESSAGES/when-command.mo

Also here, ``it.po`` and the ``/it/`` part in the folder have to be changed
according to the translated locale. In my opinion such command-line based
tools should be preferred over other utilities to create the compiled object
file, in order to avoid to save files in the wrong places or to possibly
pollute a package generated from the repository clone. However, for the
editing phase in *Step 2* any tool can be used. If ``poedit`` is chosen and
launched from the base directory of the source tree, it should automatically
recognize ``po`` as the directory containing translation files: open the one
that you would like to edit and you will be presented with a window that
allows per-string based translation. [#nonewstrings]_


Translation hints
=================

I have tried to be as consistent as possible when writing UI text and command
line output in English. Most of the times I tried to follow these basic
directions:

* I preferred US English over British (although I tend to prefer to speak
  British)
* text in dialog box labels follows (or at least should follow, I surely have
  left something out) `title case`_
* text in command line output is never capitalized, apart from the preamble
  and notes for the ``--help`` switch output, and the applet name in the
  ``--version`` output.

These guidelines should also help to recognize where a string belongs when
translating a newly created ``xx.po`` file: basically, all (or almost all)
sentences that begin with a lower case letter are used in console output, and
strings that begin with a capital letter are in almost all cases in the
graphical UI. However a translator is strongly advised to give **When** a
try, and explore its English interface (both UI and console, by testing the
CLI switches using the ``--verbose`` modifier) to be sure of what he is
translating. Also, the following command should be issued

::

  $ when-command --help

to locate text that belongs to brief command help. Please note that some words
in the help text for the ``-h`` switch cannot be modified: they are directly
handled by the Python interpreter. Some more detailed instructions follow:

1. help text for switches should remain *below 55 characters*
2. letters inside brackets in help text should not be changed
3. console output strings should remain *below 60 characters*, and consider
   that ``%s`` placeholders in some cases might be replaced by quite long
   strings (like 20 characters or so)
4. strings in ALL CAPS, numbers and mathematical symbols
   *must NOT be translated*
5. labels in dialog boxes should remain as short as possible, possibly around
   the same size as the English counterpart
6. labels that are *above* or *aside* text entries (especially the time
   specifications that appear in the *Condition Dialog Box* for time based
   conditions and the *DBus parameter* specification strings like *Value #*
   and *Sub #*) should *not* be longer than the English counterpart: use
   abbreviations if necessary
7. most of the times, entries in drop down combo boxes (such as condition
   types) *can* be somewhat longer than the English counterpart
8. keep dialog box names short
9. *button* labels *must* follow commonly used translations every time it is
   possible: for example, the *Reload* button is present in many applications
   and the most common translation should be preferred
10. menu entries that have common counterparts (such as *About...*,
    *Settings...* and *Quit*) should be translated accordingly
11. button labels should not force the growth of a button: use a different
    translation if necessary, or an abbreviation if there is no other option
12. column titles should not be much longer than the English counterparts,
    use abbreviations if necessary unless the related column is part of a
    small set (like two or three columns)
13. *title case* is definitely *not* mandatory: the most comfortable and
    pleasant casing style should be used for each language
14. try to use only special characters normally available in the default
    ASCII code page for the destination language, such as diacritics: if
    possible avoid other symbols and non-printable characters.

.. Note::
  There is one point where the translation might become difficult: the
  ``"showing %s box of currently running instance"`` *msgid*. Here ``%s`` is
  replaced with a machine-determined nickname for a dialog box. For the
  *About Dialog Box* the message would be
  ``"showing about box of currently running instance"`` and the word ``about``
  cannot be translated. Feel free to use quotes to enclose the nickname in a
  translation, if you find it necessary.

A personal hint, that I followed when translating from English to Italian, is
that when a term in one's own language is either obsolete, or unusual, or just
"funny" in the context, it has not to be necessarily preferred over a
colloquially used English counterpart. For example, the word *Desktop* is
commonly used in Italian to refer to a graphical session desktop: I would
never translate it to *Scrivania* -- which is the exact translation -- in an
application like **When**, because it would sound strange to the least.

.. _`title case`: http://www.grammar-monster.com/lessons/capital_letters_title_case.htm


.. [#nonewstrings] Consider that ``poedit`` would not show new or untranslated
  strings by default.
