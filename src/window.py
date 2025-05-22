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

from gi.repository import Adw
from gi.repository import Gtk
import os
#from vendor.simpleeval import simple_eval

from .math import Math
from .units import *
from .conversion import Conversion

@Gtk.Template(resource_path='/com/github/heidefinnischen/cuneo/window.ui')
class CuneoWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'CuneoWindow'

    # Widgets

    # Calculator Widgets
    calc_entry = Gtk.Template.Child()
    calc_result = Gtk.Template.Child()

    # Converter Widgets
    type_dropdown = Gtk.Template.Child()
    from_unit = Gtk.Template.Child()
    to_unit = Gtk.Template.Child()
    from_unit_entry = Gtk.Template.Child()
    to_unit_entry = Gtk.Template.Child()

    # General Widgets
    mode_stack = Gtk.Template.Child()
    mode_toggle = Gtk.Template.Child()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.conversion_types = CONVERSION_TYPES
        self.temperature_units = TEMPERATURE_UNITS

        model = Gtk.StringList()
        for conversion_type in self.conversion_types.keys():
            model.append(conversion_type.title())
        self.type_dropdown.set_model(model)

        # Connect signal to update the other dropdowns on change
        self.type_dropdown.connect("notify::selected", self.on_type_changed)

        # Populate initial units
        self.populate_unit_dropdowns(self.conversion_types['length'])

        self.set_resizable(False)

        self.math = Math()
        self.conversion = Conversion()


    def on_type_changed(self, dropdown, _):
        selected_index = dropdown.get_selected()
        self.from_unit_entry.set_text("")
        if selected_index < 0:
            return

        # Get the selected text from the dropdown
        selected_item = dropdown.get_model().get_item(selected_index)
        selected_type_title = selected_item.get_string()
        selected_type = selected_type_title.lower()

        units_dict = self.conversion_types.get(selected_type)
        if units_dict:
            self.populate_unit_dropdowns(units_dict)

    def populate_unit_dropdowns(self, units_dict):
        units = units_dict.keys()

        from_model = Gtk.StringList()
        to_model = Gtk.StringList()

        for unit in units:
            from_model.append(unit)
            to_model.append(unit)

        self.from_unit.set_model(from_model)
        self.to_unit.set_model(to_model)

        self.from_unit.set_selected(0)
        self.to_unit.set_selected(1 if len(units) > 1 else 0)

    def update_conversion_result(self):
        try:
            value = float(self.from_unit_entry.get_text())
        except:
            if self.from_unit_entry.get_text() == "":
                self.to_unit_entry.set_text("")
            else:
                self.to_unit_entry.set_text("Invalid")
            return

        category_model = self.type_dropdown.get_model()
        from_model = self.from_unit.get_model()
        to_model = self.to_unit.get_model()

        item = category_model.get_item(self.type_dropdown.get_selected())
        selected_category = item.get_string().lower() if item else ""

        selected_category = category_model.get_string(self.type_dropdown.get_selected())
        from_unit = from_model.get_string(self.from_unit.get_selected()).lower()
        to_unit = to_model.get_string(self.to_unit.get_selected()).lower()

        try:
            result = self.conversion.convert_value(value, from_unit, to_unit, selected_category, self.conversion_types)
            self.to_unit_entry.set_text(str(round(result, 4)))
        except Exception as e:
            print("Conversion failed:", e)
            self.to_unit_entry.set_text("Error")

    # Update UI in Converter
    @Gtk.Template.Callback()
    def on_convert_entry_changed(self, entry):
        self.update_conversion_result()

    @Gtk.Template.Callback()
    def on_to_unit_changed(self, widget, parameter):
        self.update_conversion_result()

    @Gtk.Template.Callback()
    def on_from_unit_changed(self, widget, parameter):
        self.update_conversion_result()

    # Update UI when inverting units
    @Gtk.Template.Callback()
    def on_invert_units_clicked(self, param):
        input_entry = self.from_unit_entry.get_text()
        output_entry = self.to_unit_entry.get_text()

        self.to_unit_entry.set_text(input_entry)
        self.from_unit_entry.set_text(output_entry)

        input_unit_index = self.from_unit.get_selected()
        output_unit_index = self.to_unit.get_selected()

        self.to_unit.set_selected(input_unit_index)
        self.from_unit.set_selected(output_unit_index)


    # Update Toggle
    @Gtk.Template.Callback()
    def on_toggle_changed(self, group, _):
        active = group.get_active()
        if active == 1:
            self.mode_stack.set_visible_child_name("convert")
            self.remove_css_class("smooth-transition")
            self.add_css_class("yellow-ruler")
        if active != 1:
            self.mode_stack.set_visible_child_name("calculate")
            self.add_css_class("smooth-transition")
            self.remove_css_class("yellow-ruler")


    # Update Math
    @Gtk.Template.Callback()
    def on_entry_changed(self, entry):
        expression = self.calc_entry.get_text()
        result = self.math.calculate(expression)
        self.calc_result.set_text(result)



