# main.py
#
# Copyright 2025 Jan-Niklas Kuhn
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import os
import gi
from gi.repository import Gtk, Gdk, GLib

import gettext
import locale

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

locale.setlocale(locale.LC_ALL, '')

# In Flatpak, translations are in /app/share/locale
LOCALE_DIR = '/app/share/locale'

gettext.bindtextdomain('cuneo', LOCALE_DIR)
gettext.textdomain('cuneo')
_ = gettext.gettext

from gi.repository import Gtk, Gio, Adw
from .window import CuneoWindow




class CuneoApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.heidefinnischen.cuneo',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
                         resource_base_path='/io/github/heidefinnischen/cuneo')

        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)

        self._load_css()

    def _load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource("/io/github/heidefinnischen/cuneo/style.css")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = CuneoWindow(application=self)
        win.set_size_request(400, 30)
        win.present()

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutDialog(application_name='Cuneo',
                                application_icon='io.github.heidefinnischen.cuneo',
                                developer_name='Jan-Niklas Kuhn',
                                version='0.9.0',
                                developers=['Jan-Niklas Kuhn'],
                                copyright='© 2025 Jan-Niklas Kuhn')
        # Translators: Replace "translator-credits" with your name/username, and optionally an email or URL.
        about.set_translator_credits(_('translator-credits'))
        about.set_artists(['Jan-Niklas Kuhn'])
        about.set_designers(['Jan-Niklas Kuhn'])
        about.set_issue_url('https://github.com/heidefinnischen/cuneo/issues')
        about.set_website('https://github.com/heidefinnischen/cuneo')
        about.set_license_type(3)
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

def main(version):
    """The application's entry point."""
    app = CuneoApplication()
    return app.run(sys.argv)
    
