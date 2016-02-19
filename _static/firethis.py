# file: firethis.py
# -*- coding: utf-8 -*-
#
# A very basic command-based condition plugin
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


from plugin import CommandConditionPlugin, PLUGIN_CONST, plugin_name


# if localization is supported, uncomment the lines above configure
# them as appropriate, and remove this replacement function
def _(x):
    return x


HELP = _("""\
This is a sample command based condition plugin: it will only fire when it
finds a file specified by the user (that is, created in the home directory
with this specific name but regardless of the contents).
""")


# class for a plugin: the derived class name should always be Plugin
class Plugin(CommandConditionPlugin):

    def __init__(self):
        CommandConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Fire This"),
            description=_(
                "Expect a file with specific name in the home directory"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='firethis',
            help_string=HELP,
            version="1.0.0",
        )
        # the append steps inform the plugin installer of the resource files
        self.graphics.append('firethis.png')
        self.resources.append('firethis.glade')

        # here the pane is prepared in the same way as a dialog box, but
        # it is not initialized: the initialization is deferred to the first
        # attempt to retrieve the pane
        self.builder = self.get_dialog('firethis')
        self.plugin_panel = None
        self.forward_allowed = True

        # the default command line is almost the same as before
        self.command_line = "test -f ~/'fire.this'"
        self.summary_description = \
            "On creation of a 'fire.this' file in the home directory"

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
            o('txtEntry').set_text('fire.this')
        return self.plugin_panel

    def change_entry(self, obj):
        o = self.builder.get_object
        filename = o('txtEntry').get_text()
        if filename:
            self.summary_description = _(
                "On creation of a '%s' file in the home directory") % filename
            self.command_line = "test -f ~/'%s'" % filename
            self.allow_forward(True)
        else:
            self.summary_description = None
            self.command_line = None
            self.allow_forward(False)


# end.
