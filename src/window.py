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
from gi.repository import Gtk, Gdk, GLib, Gio
from collections import defaultdict

from gettext import gettext as _

from .units import *
from .conversion import Conversion
from .magic import tokenize, Parser, evaluate, sanitize_expression, format_result, ast_to_string, replace_superscripts
from .ui import *


@Gtk.Template(resource_path='/io/github/heidefinnischen/cuneo/window.ui')
class CuneoWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'CuneoWindow'

    # Widgets

    # Calculator Widgets
    calc_entry = Gtk.Template.Child()
    calc_result = Gtk.Template.Child()
    calc_equation = Gtk.Template.Child()
    calc_equation_box = Gtk.Template.Child()
    operator_menu = Gtk.Template.Child()
    expression_button = Gtk.Template.Child()
    copy_button = Gtk.Template.Child()

    # Converter Widgets
    unit_type_button = Gtk.Template.Child()
    unit_type_popover = Gtk.Template.Child()
    unit_type_box = Gtk.Template.Child()
    unit_type_icon = Gtk.Template.Child()

    from_unit_entry = Gtk.Template.Child()
    from_unit_popover = Gtk.Template.Child()
    from_unit_box = Gtk.Template.Child()
    from_unit_label = Gtk.Template.Child()

    to_unit_entry = Gtk.Template.Child()
    to_unit_popover = Gtk.Template.Child()
    to_unit_box = Gtk.Template.Child()
    to_unit_label = Gtk.Template.Child()

    # General Widgets
    mode_stack = Gtk.Template.Child()

    calc_group = Gtk.Template.Child()
    conv_group = Gtk.Template.Child()

    headerbar = Gtk.Template.Child()
    menu_button = Gtk.Template.Child()
    window_handle = Gtk.Template.Child()





    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.conversion_types = CONVERSION_TYPES
        self.temperature_units = TEMPERATURE_UNITS

        self.set_resizable(False)

        self.conversion = Conversion()
        self.conv_group.set_group(self.calc_group)
        self.calc_group.set_active(True)
        self.state = ConverterState()

        # Set initial unit
        initial_category = 'length'
        self.state.set_category(initial_category)
        self.populate_type_buttons(initial_category)

        icon_name = UNIT_TYPE_ICONS.get(initial_category, "item-missing-symbolic") #item missing is fallback
        self.unit_type_icon.set_from_icon_name(icon_name)
        self.populate_units(self.conversion_types[initial_category], self.from_unit_box, self.on_from_unit_selected, active_unit_id=self.state.from_unit)
        self.populate_units(self.conversion_types[initial_category], self.to_unit_box, self.on_to_unit_selected, active_unit_id=self.state.to_unit)

        settings = Gtk.Settings.get_default()
        layout = settings.get_property("gtk-decoration-layout")

        # Makes calc entry auto text entry, but fix to not work after having clicked anything or while convert visible instead.

        #Make sure your window can receive focus
        self.set_focusable(True)
        self.set_can_focus(True)

        # Create and connect the key controller
        key_controller = Gtk.EventControllerKey.new()
        key_controller.connect("key-pressed", self.on_key_pressed)
        self.add_controller(key_controller)

        self._adjust_headerbar_item_position()
        self._setup_actions()


    def _setup_actions(self):
        actions = {
            "switch_mode": (self._toggle_mode, ["<Ctrl>Tab"]),
            "sqrt": (lambda action, param: self.on_btn_sqrt_clicked(None), ["<Ctrl>R"]),
        }

        for name, (callback, accels) in actions.items():
            action = Gio.SimpleAction.new(name, None)
            action.connect("activate", callback)
            self.add_action(action)
            self.get_application().set_accels_for_action(f"win.{name}", accels)

    def _toggle_mode(self, action, param):
        current = self.mode_stack.get_visible_child_name()
        if current == "convert":
            self.calc_group.set_active(True)
        else:
            self.conv_group.set_active(True)

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






################### CALCULATOR AREA

    @Gtk.Template.Callback()
    def on_copy_button_clicked(self, button):
        text = self.calc_result.get_text()
        clipboard = self.calc_result.get_display().get_clipboard()
        content_provider = Gdk.ContentProvider.new_for_value(text)
        clipboard.set_content(content_provider)

    # Update Math
    @Gtk.Template.Callback()
    def on_entry_changed(self, entry):
        raw_expression = self.calc_entry.get_text()
        expression = sanitize_expression(raw_expression)

        try:
            expression = replace_superscripts(expression)
            tokens = tokenize(expression)
            ast = Parser(tokens).parse()
            result = evaluate(ast)
            output = format_result(result)

            if output.strip() != expression.strip():
                self.calc_result.set_text(output)

                # Calculate pixel width of the text in the entry
                layout = self.calc_entry.create_pango_layout(raw_expression)
                width, _ = layout.get_pixel_size()

                # Add some padding/margin adjustment for spacing
                self.calc_equation_box.set_margin_start(width + 18)
                self.calc_equation.set_visible(True)
                self.copy_button.set_visible(True)
                self.calc_entry.add_css_class("entry-pad")
                self.calc_equation_box.add_css_class("entry-pad")
                self.expression_button.set_visible(True)


                # Update interpreted expression preview
                interpreted = ast_to_string(ast)
                self.expression_button.set_label(interpreted)

            else:
                # Hide result and UI elements if no meaningful difference
                self.calc_result.set_text("")
                self.calc_equation.set_visible(False)
                self.copy_button.set_visible(False)
                self.expression_button.set_label(error_message)

        except (SyntaxError, ValueError, ZeroDivisionError):
            self.calc_result.set_text("")
            self.expression_button.set_label(error_message)
            self.calc_equation.set_visible(False)
            self.copy_button.set_visible(False)

    def insert_operator(self, operator):
        entry = self.calc_entry
        text = entry.get_text()

        try:
            start, end = entry.get_selection_bounds()
        except Exception:
            start = end = entry.get_position()  # Fallback to cursor position

        if start != end:
            selected_text = text[start:end]
            new_text = text[:start] + f"{operator}({selected_text})" + text[end:]
            cursor_pos = start + len(f"{operator}({selected_text})")
        else:
            pos = entry.get_position()
            new_text = text[:pos] + f"{operator}()" + text[pos:]
            cursor_pos = pos + len(f"{operator}(")

        entry.set_text(new_text)
        entry.grab_focus()
        self.operator_menu.get_popover().hide()
        entry.set_position(cursor_pos)
        entry.select_region(cursor_pos, cursor_pos)

    @Gtk.Template.Callback()
    def on_btn_sqrt_clicked(self, button):
        self.insert_operator("√")

    @Gtk.Template.Callback()
    def on_btn_sin_clicked(self, button):
        self.insert_operator("sin")

    @Gtk.Template.Callback()
    def on_btn_cos_clicked(self, button):
        self.insert_operator("cos")

    @Gtk.Template.Callback()
    def on_btn_tan_clicked(self, button):
        self.insert_operator("tan")

    @Gtk.Template.Callback()
    def on_btn_log_clicked(self, button):
        self.insert_operator("log")

    def insert_constant(self, constant: str):
        entry = self.calc_entry
        text = entry.get_text()

        pos = entry.get_position()
        new_text = text[:pos] + constant + text[pos:]

        entry.set_text(new_text)
        entry.grab_focus()
        self.operator_menu.get_popover().hide()
        entry.set_position(pos + len(constant))

    @Gtk.Template.Callback()
    def on_btn_pi_clicked(self, button):
        self.insert_constant("π")

################### CONVERTER AREA

    def update_unit_labels(self):
        def get_short_unit_label(container):
            child = container.get_first_child()
            while child:
                if isinstance(child, Gtk.ToggleButton) and child.get_active():
                    label_box = child.get_child()
                    if isinstance(label_box, Gtk.Box):
                        label = label_box.get_first_child()
                        found_one = False
                        while label:
                            if isinstance(label, Gtk.Label):
                                if found_one:
                                    return label.get_text()  # This is the second label (short name)
                                found_one = True
                            label = label.get_next_sibling()
                child = child.get_next_sibling()
            return "—"

        self.from_unit_label.set_text(get_short_unit_label(self.from_unit_box))
        self.to_unit_label.set_text(get_short_unit_label(self.to_unit_box))



    def populate_units(self, units_dict, container, on_clicked_handler, active_unit_id=None):
        self.clear_container(container)

        # Group units by tag
        grouped_units = defaultdict(dict)
        for unit_id, values in units_dict.items():
            tag = values[4] if len(values) > 4 else None
            grouped_units[tag][unit_id] = values

        self.toggle_buttons = []
        first_button = None
        is_first_category = True  # Track if we’re processing the first group

        for tag, units_in_tag in grouped_units.items():
            if tag in UNIT_TAGS:
                display_name, subtitle = UNIT_TAGS[tag]
            else:
                display_name = ""
                subtitle = ""

            if not (is_first_category and tag == None):
                box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, hexpand=True)
                box.set_margin_top(6)
                box.set_margin_bottom(6)

                separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                separator.set_valign(Gtk.Align.CENTER)
                separator.set_size_request(10, 1)
                box.append(separator)

                # Main category label
                category_label = Gtk.Label(label=display_name)
                category_label.set_halign(Gtk.Align.START)
                category_label.add_css_class("caption")
                category_label.add_css_class("dimmed")
                box.append(category_label)

                separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                separator.set_hexpand(True)  # fill the remaining space
                separator.set_valign(Gtk.Align.CENTER)
                box.append(separator)

                # Subtitle label (smaller, dimmed)
                subtitle_label = Gtk.Label(label=subtitle)
                subtitle_label.set_halign(Gtk.Align.END)
                subtitle_label.add_css_class("caption")
                subtitle_label.add_css_class("dimmed")
                box.append(subtitle_label)

                separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                separator.set_valign(Gtk.Align.CENTER)
                separator.set_size_request(10, 1)
                box.append(separator)

                container.append(box)

            is_first_category = False  # After first loop

            for unit_id, values in units_in_tag.items():
                singular, plural, short = values[:3]

                button = Gtk.ToggleButton()
                button.set_name(unit_id)
                button.add_css_class("flat")

                row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, hexpand=True)
                label_left = Gtk.Label(label=plural)
                label_left.set_hexpand(True)
                label_left.set_halign(Gtk.Align.START)
                label_left.add_css_class("body")
                label_left.set_margin_end(30)

                label_right = Gtk.Label(label=short)
                label_right.set_halign(Gtk.Align.END)
                label_right.add_css_class("dimmed")

                row_box.append(label_left)
                row_box.append(label_right)
                button.set_child(row_box)

                button.connect("clicked", on_clicked_handler)

                if first_button is None:
                    first_button = button
                else:
                    button.set_group(first_button)

                if active_unit_id:
                    if unit_id == active_unit_id:
                        button.set_active(True)
                else:
                    if first_button == button:
                        button.set_active(True)

                container.append(button)
                self.toggle_buttons.append(button)

        self.update_unit_labels()



    # Update UI in Converter
    @Gtk.Template.Callback()
    def on_convert_entry_changed(self, entry):
        text = entry.get_text()
        try:
            self.state.input_value = float(text)
        except ValueError:
            self.state.input_value = None
        self.update_conversion_result()

    def on_to_unit_selected(self, button):
        unit_id = button.get_name()

        self.state.to_unit = unit_id
        self.update_unit_labels()

        self.to_unit_popover.hide()  # hide popover after selection if desired
        self.update_conversion_result()

    def on_from_unit_selected(self, button):
        unit_id = button.get_name()

        self.state.from_unit = unit_id
        self.update_unit_labels()

        self.from_unit_popover.hide()  # hide popover after selection if desired
        self.update_conversion_result()


    # Update UI when inverting units
    @Gtk.Template.Callback()
    def on_invert_units_clicked(self, param):

        self.state.invert_units()

        if self.from_unit_entry.get_text() != None and self.from_unit_entry.get_text() != "":
            self.from_unit_entry.set_text(str(self.conversion.format_conversion_result(round(self.state.input_value, 6))))
            self.to_unit_entry.set_text(str(self.conversion.format_conversion_result(round(self.state.result, 6))))

        # Update unit buttons (just by name, based on model)
        self.activate_button_by_unit(self.from_unit_box, self.state.from_unit)
        self.activate_button_by_unit(self.to_unit_box, self.state.to_unit)

        # Refresh any labels if needed
        self.update_unit_labels()

    def update_conversion_result(self):
        value = self.state.input_value
        if value is None:
            self.to_unit_entry.set_text("")
            return

        from_unit = self.state.from_unit
        to_unit = self.state.to_unit
        category = self.state.selected_category

        if not from_unit or not to_unit or not category:
            self.update_convert_result_text(None)
            return

        if value != None and value != "":
            result = self.conversion.convert_value(value, from_unit, to_unit, category, self.conversion_types)
            self.update_convert_result_text(result)



################### GENERAL AREA

    @Gtk.Template.Callback()
    def on_toggle_toggled(self, button):
        if not button.get_active():
            return  # Ignore toggled-off buttons

        if button == self.conv_group:
            self.mode_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP)
            self.mode_stack.set_visible_child_name("convert")
            self.remove_css_class("smooth-transition")
            self.add_css_class("yellow-ruler")
            self.conv_group.add_css_class("yellow-ruler-button")
        elif button == self.calc_group:
            self.mode_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_DOWN)
            self.mode_stack.set_visible_child_name("calculate")
            self.add_css_class("smooth-transition")
            self.conv_group.remove_css_class("yellow-ruler-button")
            self.remove_css_class("yellow-ruler")

    @Gtk.Template.Callback()
    def on_entry_focus(self, entry, param):
        def select_all():
            entry.select_region(0, -1)

        GLib.idle_add(select_all)


    # Can we simplify the following three into one? (Last two are almost the same but some use legacy middle def)

    def get_active_toggle_name(self, container):
        child = container.get_first_child()
        while child:
            if isinstance(child, Gtk.ToggleButton) and child.get_active():
                return child.get_name()
            child = child.get_next_sibling()
        return None

    def activate_button_by_unit(self, container, unit_name):
        child = container.get_first_child()
        while child is not None:
            if child.get_name() == unit_name:
                child.set_active(True)
                return
            child = child.get_next_sibling()





    def populate_type_buttons(self, active_type_id=None):
        # Clear previous buttons
        child = self.unit_type_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.unit_type_box.remove(child)
            child = next_child

        first_button = None
        for type_id in sorted(self.conversion_types):
            title = UNIT_TYPE_NAMES.get(type_id, type_id.title())

            label = Gtk.Label(label=title)
            label.set_halign(Gtk.Align.START)
            label.set_hexpand(True)
            label.add_css_class("body")
            label.set_margin_end(30)

            icon_name = UNIT_TYPE_ICONS.get(type_id, "item-missing-symbolic")
            icon = Gtk.Image.new_from_icon_name(icon_name)
            icon.set_halign(Gtk.Align.END)

            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            box.append(label)
            box.append(icon)

            # Create button with box as child
            button = Gtk.ToggleButton()
            button.set_name(type_id)
            button.add_css_class("flat")
            button.set_child(box)
            button.connect("clicked", self.on_type_button_clicked)

            if first_button is None:
                first_button = button
            else:
                button.set_group(first_button)

            if active_type_id:
                if type_id == active_type_id:
                    button.set_active(True)
            else:
                if first_button == button:
                    button.set_active(True)

            self.unit_type_box.append(button)

    def on_type_button_clicked(self, button):
        selected_type = button.get_name()

        self.state.set_category(selected_type)

        units_dict = self.conversion_types.get(selected_type)
        if units_dict:
            self.populate_units(units_dict, self.from_unit_box, self.on_from_unit_selected, active_unit_id=self.state.from_unit)
            self.populate_units(units_dict, self.to_unit_box, self.on_to_unit_selected, active_unit_id=self.state.to_unit)

        icon_name = UNIT_TYPE_ICONS.get(selected_type, "item-missing-symbolic") #item missing is fallback
        self.unit_type_icon.set_from_icon_name(icon_name)

        self.state.update()
        self.from_unit_entry.set_text("")
        self.to_unit_entry.set_text("")


    def on_key_pressed(self, controller, keyval, keycode, state):
        key = Gdk.keyval_name(keyval)

        # Only respond to printable characters
        if not key or len(key) != 1 or not key.isprintable():
            return False  # Let other handlers deal with it

        active_page = self.mode_stack.get_visible_child_name()

        if active_page == "calculate":
            entry = self.calc_entry
        elif active_page == "convert":
            entry = self.from_unit_entry
        else:
            return False  # Not a page we want to handle

        # If the entry doesn't already have focus, grab it
        if not entry.has_focus():
            entry.grab_focus()

        current = entry.get_text()
        entry.set_text(current + key)
        entry.set_position(-1)
        return True


    def update_convert_result_text(self, result):
        if result != None and result != "":
            try:
                self.state.result = result
                output = self.conversion.format_conversion_result(round(result, 6))
                self.to_unit_entry.set_text(str(output))
            except Exception as e:
                self.state.result = None
                print("Conversion failed:", e)
                self.to_unit_entry.set_text("")
        else:
            self.state.result = None
            self.to_unit_entry.set_text("")

    def clear_container(self, container):
        child = container.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            container.remove(child)
            child = next_child


class ConverterState:

    DEFAULT_UNITS = {
        "length": ("cm", "in"),
        "speed": ("kmh", "mph"),
        "temperature": ("c", "f"),
        "area": ("m2","ft2"),
        "time": ("h","d"),
        "mass": ("kg","lb"),
        "volume": ("l","gal"),
        "data": ("mb","mbit"),
        "pressure": ("bar","psi"),
        "energy": ("j","cal"),
        "frequency": ("hz","rpm"),
    }

    def __init__(self):
        self.selected_category = 'length' #Fallback
        self.input_value = None
        self.result = None
        self.update()

    def update(self):
        self.from_unit, self.to_unit = self.DEFAULT_UNITS.get(self.selected_category, ("", ""))
        self.input_value = ""
        self.result = ""

    def set_category(self, category):
        self.selected_category = category
        self.update()

    def invert_units(self):
        self.from_unit, self.to_unit = self.to_unit, self.from_unit
        self.input_value, self.result = self.result, self.input_value


