# window.py
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

from gettext import gettext as _

from gi.repository import Adw
from gi.repository import Gtk, Gdk, GLib, Gio

from .conversion_page import ConversionPage, ConverterState
from .calculation_page import CalculationPage
from .history_window import HistoryWindow

@Gtk.Template(resource_path='/io/github/heidefinnischen/cuneo/window.ui')
class CuneoWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'CuneoWindow'

    # Header Bar and Items
    headerbar = Gtk.Template.Child()
    menu_button = Gtk.Template.Child()
    window_handle = Gtk.Template.Child()

    # Stack and Stack toggles
    mode_stack = Gtk.Template.Child()
    calc_toggle = Gtk.Template.Child()
    conv_toggle = Gtk.Template.Child()

    # Stack page content
    convert_box = Gtk.Template.Child()
    calculate_box = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_resizable(False)

        # Initialize Toggle group and set default page
        self.conv_toggle.set_group(self.calc_toggle)
        self.calc_toggle.set_active(True)

        # Add page content
        self.calc_page = CalculationPage(main_window=self)
        self.calculate_box.append(self.calc_page)
        self.conv_page = ConversionPage(main_window=self)
        self.convert_box.append(self.conv_page)

        settings = Gtk.Settings.get_default()
        layout = settings.get_property("gtk-decoration-layout")

        # Create and connect the key controller
        key_controller = Gtk.EventControllerKey.new()
        key_controller.connect("key-pressed", self.on_key_pressed)
        self.add_controller(key_controller)

        self._adjust_headerbar_item_position()
        self._setup_actions()

        # Create open history action
        action = Gio.SimpleAction.new("show-history", None)
        action.connect("activate", self.on_show_history)
        self.add_action(action)
        self.connect("close-request", self.on_close)

        self.history_window = None

    def on_show_history(self, action, param):
        if not getattr(self, "history_window", None) or not self.history_window.get_visible():
            self.history_window = HistoryWindow(app=self.get_application(), main_window=self)

        self.history_window.populate_calc_history(self.calc_page.calculation_history)
        self.history_window.populate_conv_history(self.conv_page.conversion_history)
        if self.mode_stack.get_visible_child_name() == "convert":
            self.history_window.update_visible_stack("convert_history")
        else:
            self.history_window.update_visible_stack("calculate_history")
        self.history_window.present()
        self.adjust_history_headerbar_item_order()

    def _setup_actions(self):
        actions = {
            "switch_mode": (self._toggle_mode, ["<Ctrl>Tab"]),
            "invert": (
                lambda action, param: self.conv_page.on_invert_units_clicked(None)
                if self.mode_stack.get_visible_child_name() == "convert"
                else None,
                ["<Ctrl>I"]
            ),
            "sqrt": (
                lambda action, param: self.calc_page.on_btn_sqrt_clicked(None)
                if self.mode_stack.get_visible_child_name() == "calculate"
                else None,
                ["<Alt>R"]
            ),
            "sin": (
                lambda action, param: self.calc_page.on_btn_sin_clicked(None)
                if self.mode_stack.get_visible_child_name() == "calculate"
                else None,
                ["<Alt>S"]
            ),
            "cos": (
                lambda action, param: self.calc_page.on_btn_cos_clicked(None)
                if self.mode_stack.get_visible_child_name() == "calculate"
                else None,
                ["<Alt>C"]
            ),
            "tan": (
                lambda action, param: self.calc_page.on_btn_tan_clicked(None)
                if self.mode_stack.get_visible_child_name() == "calculate"
                else None,
                ["<Alt>T"]
            ),
            "log": (
                lambda action, param: self.calc_page.on_btn_log_clicked(None)
                if self.mode_stack.get_visible_child_name() == "calculate"
                else None,
                ["<Alt>L"]
            ),
            "pi": (
                lambda action, param: self.calc_page.on_btn_pi_clicked(None)
                if self.mode_stack.get_visible_child_name() == "calculate"
                else None,
                ["<Alt>P"]
            ),
            "show_history": (self.on_show_history, ["<Ctrl>H"]),
        }

        for name, (callback, accels) in actions.items():
            action = Gio.SimpleAction.new(name, None)
            action.connect("activate", callback)
            self.add_action(action)
            self.get_application().set_accels_for_action(f"win.{name}", accels)

    def _toggle_mode(self, action, param): # Keyboard Shortcut only code
        current = self.mode_stack.get_visible_child_name()
        if current == "convert":
            self.calc_toggle.set_active(True)
        else:
            self.conv_toggle.set_active(True)

    def _is_close_button_on_left(self):
        settings = Gtk.Settings.get_default()
        layout = settings.get_property("gtk-decoration-layout")
        if layout:
            left, _, _ = layout.partition(':')
            return 'close' in left.split(',')
        return False

    def _adjust_headerbar_item_position(self):
        if self._is_close_button_on_left():
            # Close button on right: move menu_box from end to start
            # Remove from current parent first

            parent = self.window_handle.get_parent()
            if parent:
                parent.remove(self.window_handle)
            self.headerbar.pack_end(self.window_handle)

            parent = self.menu_button.get_parent()
            if parent:
                parent.remove(self.menu_button)
            self.headerbar.pack_end(self.menu_button)

            self.mode_stack.remove_css_class("right-margin-button")


    def adjust_history_headerbar_item_order(self):
        if self._is_close_button_on_left():
            parent = self.history_window.clear_button.get_parent()
            if parent:
                parent.remove(self.history_window.clear_button)
            self.history_window.headerbar.pack_end(self.history_window.clear_button)

    @Gtk.Template.Callback()
    def on_toggle_toggled(self, button):
        if not button.get_active():
            return  # Ignore toggled-off buttons

        if button == self.conv_toggle:
            self.mode_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP)
            self.mode_stack.set_visible_child_name("convert")
            self.remove_css_class("smooth-transition")
            self.add_css_class("yellow-ruler")
            if self.history_window:
                self.history_window.update_visible_stack("convert_history")
        elif button == self.calc_toggle:
            self.mode_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_DOWN)
            self.mode_stack.set_visible_child_name("calculate")
            self.add_css_class("smooth-transition")
            self.remove_css_class("yellow-ruler")
            if self.history_window:
                self.history_window.update_visible_stack("calculate_history")

    def on_key_pressed(self, controller, keyval, keycode, state):
        key = Gdk.keyval_name(keyval)

        # Only respond to printable characters
        if not key or len(key) != 1 or not key.isprintable():
            return False  # Let other handlers deal with it

        active_page = self.mode_stack.get_visible_child_name()

        if active_page == "convert":
            entry = self.conv_page.from_unit_entry
        else:
            entry = self.calc_page.calc_entry

        # If the entry doesn't already have focus, grab it
        if not entry.has_focus():
            entry.grab_focus()

        current = entry.get_text()
        entry.set_text(current + key)
        entry.set_position(-1)
        return True

    def on_close(self, *args):
        if self.history_window and self.history_window.get_visible():
            self.history_window.close()
        return False  # allow normal window close

